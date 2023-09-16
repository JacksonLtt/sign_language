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

#define NUMBER_OF_SENSORS 6
ICM_20948_SPI **ICM20948_Sensor; //Create pointer to a set of pointers to the sensor class
String name_imu[6] = {"ICM_1", "ICM_2", "ICM_3", "ICM_4", "ICM_5", "ICM_6"};
int CS_PIN[6] = {2, 3, 4, 5, 28, 29};


#include <bluefruit.h> // BLE
BLEDis bledis;
BLEUart bleuart;
int COUNT = 0;
String device_name = "left#2";
uint32_t rxCount = 0;
uint32_t rxStartTime = 0;
uint32_t rxLastTime = 0;
int send_request = 0;
int count_num = 0;

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
  init_icm(ICM20948_Sensor[5], 5);


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
  Bluefruit.setName("left#2");
  Serial.println(device_name);
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

  //  rxCount += count;
  Serial.print(count);
  if (count == 2) {
    uint8_t ch;
    ch = (uint8_t) bleuart.read();
    Serial.write(ch);
    Serial.println();
    if ( ch == (uint8_t)'s' or ch == (uint8_t)'r' or ch == (uint8_t)'t' or ch == (uint8_t)'c') {
      Serial.println("\nstart_send");
      send_request = 1;
      Serial.print("send_request:");
      Serial.println(send_request);
      count_num = 0;

    }
    else if (ch == (uint8_t)'e') {
      Serial.println("\nend_send");
      send_request = 0;
      Serial.print("send_request:");
      Serial.println(send_request);

    }
  }
  //  Serial.println()
  bleuart.flush(); // empty rx fifo

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

  // Here we are doing a SW reset to make sure the device starts in a known state
  sensor->swReset();
  if (sensor->status != ICM_20948_Stat_Ok)
  {
    Serial.print(F("Software Reset returned: "));
    Serial.println(sensor->statusString());
  }
  delay(250);

  // Now wake the sensor up
  sensor->sleep(false);
  sensor->lowPower(false);

  // The next few configuration functions accept a bit-mask of sensors for which the settings should be applied.

  // Set Gyro and Accelerometer to a particular sample mode
  // options: ICM_20948_Sample_Mode_Continuous
  //          ICM_20948_Sample_Mode_Cycled
  sensor->setSampleMode((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), ICM_20948_Sample_Mode_Continuous);
  if (sensor->status != ICM_20948_Stat_Ok)
  {
    Serial.print(F("setSampleMode returned: "));
    Serial.println(sensor->statusString());
  }

  // Set full scale ranges for both acc and gyr
  ICM_20948_fss_t myFSS; // This uses a "Full Scale Settings" structure that can contain values for all configurable sensors

  myFSS.a = gpm16; // (ICM_20948_ACCEL_CONFIG_FS_SEL_e)
  // gpm2
  // gpm4
  // gpm8
  // gpm16

  myFSS.g = dps2000; // (ICM_20948_GYRO_CONFIG_1_FS_SEL_e)
  // dps250
  // dps500
  // dps1000
  // dps2000

  sensor->setFullScale((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS);
  if (sensor->status != ICM_20948_Stat_Ok)
  {
    Serial.print(F("setFullScale returned: "));
    Serial.println(sensor->statusString());
  }

  // Set up Digital Low-Pass Filter configuration
  ICM_20948_dlpcfg_t myDLPcfg;    // Similar to FSS, this uses a configuration structure for the desired sensors
  myDLPcfg.a = acc_d246bw_n265bw; // (ICM_20948_ACCEL_CONFIG_DLPCFG_e)
  // acc_d246bw_n265bw      - means 3db bandwidth is 246 hz and nyquist bandwidth is 265 hz
  // acc_d111bw4_n136bw
  // acc_d50bw4_n68bw8
  // acc_d23bw9_n34bw4
  // acc_d11bw5_n17bw
  // acc_d5bw7_n8bw3        - means 3 db bandwidth is 5.7 hz and nyquist bandwidth is 8.3 hz
  // acc_d473bw_n499bw

  myDLPcfg.g = gyr_d196bw6_n229bw8; // (ICM_20948_GYRO_CONFIG_1_DLPCFG_e)
  // gyr_d196bw6_n229bw8
  // gyr_d151bw8_n187bw6
  // gyr_d119bw5_n154bw3
  // gyr_d51bw2_n73bw3
  // gyr_d23bw9_n35bw9
  // gyr_d11bw6_n17bw8
  // gyr_d5bw7_n8bw9
  // gyr_d361bw4_n376bw5

  sensor->setDLPFcfg((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myDLPcfg);
  if (sensor->status != ICM_20948_Stat_Ok)
  {
    Serial.print(F("setDLPcfg returned: "));
    Serial.println(sensor->statusString());
  }

  // Choose whether or not to use DLPF
  // Here we're also showing another way to access the status values, and that it is OK to supply individual sensor masks to these functions
  ICM_20948_Status_e accDLPEnableStat = sensor->enableDLPF(ICM_20948_Internal_Acc, false);
  ICM_20948_Status_e gyrDLPEnableStat = sensor->enableDLPF(ICM_20948_Internal_Gyr, false);
  Serial.print(F("Enable DLPF for Accelerometer returned: "));
  Serial.println(sensor->statusString(accDLPEnableStat));
  Serial.print(F("Enable DLPF for Gyroscope returned: "));
  Serial.println(sensor->statusString(gyrDLPEnableStat));

  // Choose whether or not to start the magnetometer
  sensor->startupMagnetometer();
  if (sensor->status != ICM_20948_Stat_Ok)
  {
    Serial.print(F("startupMagnetometer returned: "));
    Serial.println(sensor->statusString());
  }

  Serial.println();
  Serial.println(F("Configuration complete!"));
}

void update_to_all_imu(ICM_20948_SPI *sensor, int index) {
  // wrist x,y-> -x, -y

  if (index == 0) {
    ALL_IMU[index * 9] = sensor->accX() * 0.01 * -1;
    ALL_IMU[index * 9 + 1] = sensor->accY() * 0.01 * -1;
    ALL_IMU[index * 9 + 2] = sensor->accZ() * 0.01 * 1;



    ALL_IMU[index * 9 + 3] = sensor->magX() * -1;
    ALL_IMU[index * 9 + 4] = sensor->magY() * -1;
    ALL_IMU[index * 9 + 5] = sensor->magZ() * 1;


    ALL_IMU[index * 9 + 6] = sensor->gyrX() * -1;
    ALL_IMU[index * 9 + 7] = sensor->gyrY() * -1;
    ALL_IMU[index * 9 + 8] = sensor->gyrZ() * 1;
  }
  else {
    ALL_IMU[index * 9] = sensor->accX() * 0.01;
    ALL_IMU[index * 9 + 1] = sensor->accY() * 0.01;
    ALL_IMU[index * 9 + 2] = sensor->accZ() * 0.01;



    ALL_IMU[index * 9 + 3] = sensor->magX();
    ALL_IMU[index * 9 + 4] = sensor->magY();
    ALL_IMU[index * 9 + 5] = sensor->magZ();


    ALL_IMU[index * 9 + 6] = sensor->gyrX();
    ALL_IMU[index * 9 + 7] = sensor->gyrY();
    ALL_IMU[index * 9 + 8] = sensor->gyrZ();

  }

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


void clear_all_imu() {
  for (int i = 0; i < 55; i++) {
    ALL_IMU[i] = 0;
  }
}
void loop()
{

  // receive command from macbook while keeping connection with receiver second
  // make receiver as master and make sensor as slaves first

  if (Bluefruit.connected() && send_request == 1)
  {
    send_time = millis();


    update_imu(ICM20948_Sensor[0], 0);
    update_imu(ICM20948_Sensor[1], 1);
    update_imu(ICM20948_Sensor[2], 2);
    update_imu(ICM20948_Sensor[3], 3);
    update_imu(ICM20948_Sensor[4], 4);
    update_imu(ICM20948_Sensor[5], 5);

    ALL_IMU[54] = send_time;

    send_message();
    clear_all_imu();

    count_num += 1;
    Serial.println(count_num);
  }

  if (!Bluefruit.connected()) {
    count_num = 0;
    send_request = 0;
  }

  delay(10);
}

void print_all_imu() {
  Serial.print("[");
  for (int i = 0; i < 55; i++) {
    Serial.print(ALL_IMU[i]); Serial.print(",");
  }
  Serial.println("]");
}

void send_message(void)
{
  int packet_size = 54;
  int total_size = (packet_size + 1) * 4;
  byte byteArray[total_size];// 10+1


  for (int i = 0; i < 55; i++) {
    byteArray[i * 4] = ((uint8_t*)&ALL_IMU[i])[0];
    byteArray[i * 4 + 1] = ((uint8_t*)&ALL_IMU[i])[1];
    byteArray[i * 4 + 2] = ((uint8_t*)&ALL_IMU[i])[2];
    byteArray[i * 4 + 3] = ((uint8_t*)&ALL_IMU[i])[3];
  }

  //  byteArray[packet_size * 4] = ((uint8_t*)&send_time)[0];
  //  byteArray[packet_size * 4 + 1] = ((uint8_t*)&send_time)[1];
  //  byteArray[packet_size * 4 + 2] = ((uint8_t*)&send_time)[2];
  //  byteArray[packet_size * 4 + 3] = ((uint8_t*)&send_time)[3];



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
