/****************************************************************
   Example1_Basics.ino
   ICM 20948 Arduino Library Demo
   Use the default configuration to stream 9-axis IMU data
   Owen Lyke @ SparkFun Electronics
   Original Creation Date: April 17 2019

   Please see License.md for the license information.

   Distributed as-is; no warranty is given.
 ***************************************************************/
#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU
#include <SPI.h>

#define NUMBER_OF_SENSORS 5
ICM_20948_SPI **ICM20948_Sensor; //Create pointer to a set of pointers to the sensor class
String name_imu[6] = {"ICM_1", "ICM_2", "ICM_3", "ICM_4", "ICM_5", "ICM_6"};
int CS_PIN[5] = {2, 3, 4, 5, 28};


#include <bluefruit.h> // BLE
BLEDis bledis;
BLEUart bleuart;
int COUNT = 0;

uint32_t rxCount = 0;
uint32_t rxStartTime = 0;
uint32_t rxLastTime = 0;


float send_time = micros();
float ALL_IMU[55] = {
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time
};

void setup()
{
  Serial.begin(115200);
  SPI.begin();
  SPI.beginTransaction(SPISettings(7000000, MSBFIRST, SPI_MODE1));

  ICM20948_Sensor = new ICM_20948_SPI *[NUMBER_OF_SENSORS];

  for (int x = 0; x < NUMBER_OF_SENSORS; x++)
    ICM20948_Sensor[x] = new ICM_20948_SPI();

  init_icm(ICM20948_Sensor[0], 0);
  init_icm(ICM20948_Sensor[1], 1);
  init_icm(ICM20948_Sensor[2], 2);
  init_icm(ICM20948_Sensor[3], 3);
  init_icm(ICM20948_Sensor[4], 4);


  while ( !Serial ) delay(10);   // for nrf52840 with native usb

  Serial.println("Bluefruit52 Throughput Example");
  Serial.println("------------------------------\n");

  // Setup the BLE LED to be enabled on CONNECT
  // Note: This is actually the default behaviour, but provided
  // here in case you want to control this manually via PIN 19
  Bluefruit.autoConnLed(true);

  // Config the peripheral connection with maximum bandwidth
  // more SRAM required by SoftDevice
  // Note: All config***() function must be called before begin()
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);

  Bluefruit.begin();
  Bluefruit.setTxPower(4);    // Check bluefruit.h for supported values
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);
  Bluefruit.Periph.setConnInterval(6, 12); // 7.5 - 15 ms

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();

  // Configure and Start BLE Uart Service
  bleuart.begin();

  bleuart.setRxCallback(bleuart_rx_callback);
  bleuart.setNotifyCallback(bleuart_notify_callback);

  // Set up and start advertising
  startAdv();
}


void startAdv(void)
{
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);

  // There is no room for Name in Advertising packet
  // Use Scan response for Name
  Bluefruit.ScanResponse.addName();

  /* Start Advertising
     - Enable auto advertising if disconnected
     - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
     - Timeout for fast mode is 30 seconds
     - Start(timeout) with timeout = 0 will advertise forever (until connected)

     For recommended advertising interval
     https://developer.apple.com/library/content/qa/qa1931/_index.html
  */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

void connect_callback(uint16_t conn_handle)
{
  BLEConnection* conn = Bluefruit.Connection(conn_handle);
  Serial.println("Connected");

  // request PHY changed to 2MB
  Serial.println("Request to change PHY");
  conn->requestPHY();

  // request to update data length
  Serial.println("Request to change Data Length");
  conn->requestDataLengthUpdate();

  // request mtu exchange
  Serial.println("Request to change MTU");
  conn->requestMtuExchange(247);

  // request connection interval of 7.5 ms
  //conn->requestConnectionParameter(6); // in unit of 1.25

  // delay a bit for all the request to complete
  delay(1000);
}


void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  Serial.println();
  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}

void bleuart_rx_callback(uint16_t conn_hdl)
{
  (void) conn_hdl;

  rxLastTime = micros();

  // first packet
  if ( rxCount == 0 )
  {
    rxStartTime = micros();
  }

  uint32_t count = bleuart.available();

  rxCount += count;
  bleuart.flush(); // empty rx fifo

  // Serial.printf("RX %d bytes\n", count);
}

void bleuart_notify_callback(uint16_t conn_hdl, bool enabled)
{
  if ( enabled )
  {
    Serial.println("Send a key and press enter to start test");
  }
}


void init_icm(ICM_20948_SPI *sensor, int index) {
  Serial.print("begin ----------------------------");
  Serial.println(name_imu[index]);
  bool initialized = false;
  sensor->enableDebugging(); // Uncomment this line to enable helpful debug messages on Seria
  while (!initialized)
  {
    Serial.print("begin ");
    Serial.println(name_imu[index]);
    sensor->begin(CS_PIN[index], SPI);

    sensor->startupDefault(false); // Force a full - not minimal - startup
    Serial.print(F("Initialization of the sensor returned: "));
    Serial.println(sensor->statusString());
    if (sensor->status != ICM_20948_Stat_Ok)
    {
      Serial.println("Trying again...");
      delay(500);
    }
    else
    {
      initialized = true;
    }
  }
}

void update_to_all_imu(ICM_20948_SPI *sensor, int index) {

  //  float accx = sensor->accX() * 0.01;
  //  float accy = sensor->accY() * 0.01;
  //  float accz = sensor->accZ() * 0.01;
  //  float gyrox = sensor->gyrX();
  //  float gyroy = sensor->gyrY();
  //  float gyroz = sensor->gyrZ();
  //  float magx = sensor->magX();
  //  float magy = sensor->magY();
  //  float magz = sensor->magZ();

  ALL_IMU[index * 6] = sensor->accX() * 0.01;
  ALL_IMU[index * 6 + 1] = sensor->accY() * 0.01;
  ALL_IMU[index * 6 + 2] = sensor->accZ() * 0.01;

  ALL_IMU[index * 6 + 3] = sensor->gyrX();
  ALL_IMU[index * 6 + 4] = sensor->gyrY();
  ALL_IMU[index * 6 + 5] = sensor->gyrZ();

  ALL_IMU[index * 6 + 6] = sensor->magX();
  ALL_IMU[index * 6 + 7] = sensor->magY();
  ALL_IMU[index * 6 + 8] = sensor->magZ();
}

void update_imu(ICM_20948_SPI *sensor, int index) {
  //  Serial.print("begin ");
  //  Serial.println(name_imu[index]);
  unsigned long init_time = micros();
  if (sensor->dataReady())
  {
    sensor->getAGMT();         // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    //    printScaledAGMT(sensor); // This function takes into account the scale settings from when the measurement was made to calculate the values with units
    //    getScaledAGMT(sensor);
    //    delay(1);
    update_to_all_imu(sensor, index);
  }
  else
  {
    Serial.println("Waiting for data");
    delay(500);
  }
  //  Serial.print("diff: ");
  //  Serial.println(micros() - init_time);
}

void loop()
{



  if (Bluefruit.connected() && bleuart.notifyEnabled())
  {
    send_time = micros();


    update_imu(ICM20948_Sensor[0], 0);
    update_imu(ICM20948_Sensor[1], 1);
    update_imu(ICM20948_Sensor[2], 2);
    update_imu(ICM20948_Sensor[3], 3);
    update_imu(ICM20948_Sensor[4], 4);

    send_message();
    COUNT += 1;
    Serial.println(COUNT);
  }

  if (!Bluefruit.connected()) {
    COUNT = 0;
  }
}


void send_message(void)
{
  int packet_size = 54;
  int total_size = (packet_size + 1) * 4;
  byte byteArray[total_size];// 10+1

  Serial.print("[");
  for (int i = 0; i < 55; i++) {
    Serial.print(ALL_IMU[i]);
  }
  Serial.println("]");
  for (int i = 0; i < packet_size; i++) {
    byteArray[i * 4] = ((uint8_t*)&ALL_IMU[i])[0];
    byteArray[i * 4 + 1] = ((uint8_t*)&ALL_IMU[i])[1];
    byteArray[i * 4 + 2] = ((uint8_t*)&ALL_IMU[i])[2];
    byteArray[i * 4 + 3] = ((uint8_t*)&ALL_IMU[i])[3];
  }

  byteArray[packet_size * 4] = ((uint8_t*)&send_time)[0];
  byteArray[packet_size * 4 + 1] = ((uint8_t*)&send_time)[1];
  byteArray[packet_size * 4 + 2] = ((uint8_t*)&send_time)[2];
  byteArray[packet_size * 4 + 3] = ((uint8_t*)&send_time)[3];



  size_t sent_data_size = bleuart.write(byteArray, sizeof(byteArray));

}

void getScaledAGMT(ICM_20948_SPI *sensor)
{

  float accx = sensor->accX() * 0.01;

  float accy = sensor->accY() * 0.01;


  float accz = sensor->accZ() * 0.01;

  float gyrox = sensor->gyrX();

  float gyroy = sensor->gyrY();


  float gyroz = sensor->gyrZ();

  float magx = sensor->magX();


  float magy = sensor->magY();

  float magz = sensor->magZ();
}

void printScaledAGMT(ICM_20948_SPI *sensor)
{
  Serial.print("Scaled. Acc (mg) [ ");
  Serial.print(sensor->accX() * 0.01);
  Serial.print(", ");
  Serial.print(sensor->accY() * 0.01);
  Serial.print(", ");

  Serial.print(sensor->accZ() * 0.01);
  Serial.print(" ], Gyr (DPS) [ ");

  Serial.print(sensor->gyrX());
  Serial.print(", ");

  Serial.print(sensor->gyrY());
  Serial.print(", ");

  Serial.print(sensor->gyrZ());
  Serial.print(" ], Mag (uT) [ ");

  Serial.print(sensor->magX());
  Serial.print(", ");

  Serial.print(sensor->magY());
  Serial.print(", ");

  Serial.print(sensor->magZ());
  Serial.print(" ], Tmp (C) [ ");

  Serial.print(sensor->temp());
  Serial.print(" ]");
  Serial.println();
}
