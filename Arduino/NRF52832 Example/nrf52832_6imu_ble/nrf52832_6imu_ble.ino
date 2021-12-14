/*********************************************************************
  This is an example for our nRF52 based Bluefruit LE modules

  Pick one up today in the adafruit shop!

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  MIT license, check LICENSE for more information
  All text above, and the splash screen below must be included in
  any redistribution
*********************************************************************/

#include <bluefruit.h>

/* Best result is
    - 8.74 KB/s with 20 ms, MTU = 23
    - 23.62 KB/s with 7.5 ms, MTU = 23
    - 47.85 KB/s with 15 ms, MTU = 247
*/



BLEDis bledis;
BLEUart bleuart;

uint32_t rxCount = 0;
uint32_t rxStartTime = 0;
uint32_t rxLastTime = 0;


// Libraries for ICM 20948
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SparkFun_I2C_Mux_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_I2C_Mux
QWIICMUX myMux;

#define NUMBER_OF_SENSORS 6
Adafruit_ICM20948 **ICM20948_Sensor; //Create pointer to a set of pointers to the sensor class
String name_imu[] = {"ICM_1", "ICM_2", "ICM_3", "ICM_4", "ICM_5", "ICM_6"};
// I2C Setting
/*** I2C_SDA, I2C_SCL
   (33,32) I2C bus for icm_1 & icm_2
   (33,32) I2C bus for icm_1 & icm_2
***/
uint8_t I2C_SDA_1 = 25;
uint8_t I2C_SCL_1 = 26;

TwoWire *I2CICM_1 = &Wire;


// Liraries for Json
#include "ArduinoJson.h"
float init_time_1;
float init_time_2;

int COUNT;



/**************************************************************************/
/*!
    @brief  Sets up the HW an the BLE module (this function is called
            automatically on startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  while ( !Serial ) delay(10);   // for nrf52840 with native usb

  Serial.println("Qwiic Mux Shield Read Example");

  I2CICM_1->setClock(400000);
  I2CICM_1->setPins(I2C_SDA_1, I2C_SCL_1);
  I2CICM_1->begin();
  Wire.begin();

  //Create set of pointers to the class
  ICM20948_Sensor = new Adafruit_ICM20948 *[NUMBER_OF_SENSORS];

  //Assign pointers to instances of the class
  for (int x = 0; x < NUMBER_OF_SENSORS; x++)
    ICM20948_Sensor[x] = new Adafruit_ICM20948();

  if (myMux.begin(0x70, *I2CICM_1) == false)
  {
    Serial.println("Mux not detected. Freezing...");
    while (1)
      ;
  }
  Serial.println("Mux detected");


  byte currentPortNumber = myMux.getPort();
  Serial.print("CurrentPort: ");
  Serial.println(currentPortNumber);

  //Initialize all the sensors
  bool initSuccess = true;

  myMux.setPort(0);
  if (!ICM20948_Sensor[0]->begin_I2C(0X69, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[0]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[0]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[0]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[0]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[0]);
    Serial.println(" configured");
  }

  if (!ICM20948_Sensor[1]->begin_I2C(0X68, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[1]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[1]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[1]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[1]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[1]);
    Serial.println(" configured");
  }

  myMux.setPort(1);
  if (!ICM20948_Sensor[2]->begin_I2C(0X68, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[2]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[2]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[2]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[2]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[2]);
    Serial.println(" configured");
  }

  if (!ICM20948_Sensor[3]->begin_I2C(0X69, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[3]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[3]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[3]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[3]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[3]);
    Serial.println(" configured");
  }

  myMux.setPort(2);
  if (!ICM20948_Sensor[4]->begin_I2C(0X68, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[4]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[4]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[4]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[4]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[4]);
    Serial.println(" configured");
  }

  if (!ICM20948_Sensor[5]->begin_I2C(0X69, I2CICM_1)) //Begin returns 0 on a good init
  {
    Serial.print("Sensor ");
    Serial.print(name_imu[5]);
    Serial.println(" did not begin! Check wiring");
    initSuccess = false;
  }
  else
  {
    //Configure each sensor
    ICM20948_Sensor[5]->setAccelRange(ICM20948_ACCEL_RANGE_2_G);
    ICM20948_Sensor[5]->setGyroRange(ICM20948_GYRO_RANGE_250_DPS);
    ICM20948_Sensor[5]->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); //Write configuration bytes to initiate measurement
    Serial.print("Sensor ");
    Serial.print(name_imu[5]);
    Serial.println(" configured");
  }

  if (initSuccess == false)
  {
    Serial.print("Freezing...");
    while (1)
      ;
  }

  Serial.println("Mux Shield online");
  
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

/**
   Callback invoked when a connection is dropped
   @param conn_handle connection where this event happens
   @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
*/
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;
  Serial.print("total count:");
  Serial.println(COUNT);
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


void test_throughput(void)
{

  init_time_1 = micros();

  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t mag;
  sensors_event_t temp;

  myMux.setPort(0);
  ICM20948_Sensor[0]->getEvent(&accel, &gyro, &temp, &mag);

  float accel_x_0 = accel.acceleration.x;
  float accel_y_0 = accel.acceleration.y;
  float accel_z_0 = accel.acceleration.z;

  float mag_x_0 = mag.magnetic.x;
  float mag_y_0 = mag.magnetic.y;
  float mag_z_0 = mag.magnetic.z;

  float gyro_x_0 = gyro.gyro.x;
  float gyro_y_0 = gyro.gyro.y;
  float gyro_z_0 = gyro.gyro.z;

  ICM20948_Sensor[1]->getEvent(&accel, &gyro, &temp, &mag);

  float accel_x_1 = accel.acceleration.x;
  float accel_y_1 = accel.acceleration.y;
  float accel_z_1 = accel.acceleration.z;

  float mag_x_1 = mag.magnetic.x;
  float mag_y_1 = mag.magnetic.y;
  float mag_z_1 = mag.magnetic.z;

  float gyro_x_1 = gyro.gyro.x;
  float gyro_y_1 = gyro.gyro.y;
  float gyro_z_1 = gyro.gyro.z;

  myMux.setPort(1);
  ICM20948_Sensor[2]->getEvent(&accel, &gyro, &temp, &mag);
  float accel_x_2 = accel.acceleration.x;
  float accel_y_2 = accel.acceleration.y;
  float accel_z_2 = accel.acceleration.z;

  float mag_x_2 = mag.magnetic.x;
  float mag_y_2 = mag.magnetic.y;
  float mag_z_2 = mag.magnetic.z;

  float gyro_x_2 = gyro.gyro.x;
  float gyro_y_2 = gyro.gyro.y;
  float gyro_z_2 = gyro.gyro.z;

  ICM20948_Sensor[3]->getEvent(&accel, &gyro, &temp, &mag);
  float accel_x_3 = accel.acceleration.x;
  float accel_y_3 = accel.acceleration.y;
  float accel_z_3 = accel.acceleration.z;

  float mag_x_3 = mag.magnetic.x;
  float mag_y_3 = mag.magnetic.y;
  float mag_z_3 = mag.magnetic.z;

  float gyro_x_3 = gyro.gyro.x;
  float gyro_y_3 = gyro.gyro.y;
  float gyro_z_3 = gyro.gyro.z;


  myMux.setPort(2);
  ICM20948_Sensor[4]->getEvent(&accel, &gyro, &temp, &mag);
  float accel_x_4 = accel.acceleration.x;
  float accel_y_4 = accel.acceleration.y;
  float accel_z_4 = accel.acceleration.z;

  float mag_x_4 = mag.magnetic.x;
  float mag_y_4 = mag.magnetic.y;
  float mag_z_4 = mag.magnetic.z;

  float gyro_x_4 = gyro.gyro.x;
  float gyro_y_4 = gyro.gyro.y;
  float gyro_z_4 = gyro.gyro.z;

  ICM20948_Sensor[5]->getEvent(&accel, &gyro, &temp, &mag);
  float accel_x_5 = accel.acceleration.x;
  float accel_y_5 = accel.acceleration.y;
  float accel_z_5 = accel.acceleration.z;

  float mag_x_5 = mag.magnetic.x;
  float mag_y_5 = mag.magnetic.y;
  float mag_z_5 = mag.magnetic.z;

  float gyro_x_5 = gyro.gyro.x;
  float gyro_y_5 = gyro.gyro.y;
  float gyro_z_5 = gyro.gyro.z;

  float ALL_IMU[] = {
    accel_x_0, accel_y_0, accel_z_0, mag_x_0, mag_y_0, mag_z_0, gyro_x_0, gyro_y_0, gyro_z_0,
    accel_x_1, accel_y_1, accel_z_1, mag_x_1, mag_y_1, mag_z_1, gyro_x_1, gyro_y_1, gyro_z_1,
    accel_x_2, accel_y_2, accel_z_2, mag_x_2, mag_y_2, mag_z_2, gyro_x_2, gyro_y_2, gyro_z_2,
    accel_x_3, accel_y_3, accel_z_3, mag_x_3, mag_y_3, mag_z_3, gyro_x_3, gyro_y_3, gyro_z_3,
    accel_x_4, accel_y_4, accel_z_4, mag_x_4, mag_y_4, mag_z_4, gyro_x_4, gyro_y_4, gyro_z_4,
    accel_x_5, accel_y_5, accel_z_5, mag_x_5, mag_y_5, mag_z_5, gyro_x_5, gyro_y_5, gyro_z_5,
    init_time_1
  };
  init_time_2 = micros();

  int packet_size = 54;
  int total_size = (packet_size + 1) * 4;
  byte byteArray[total_size];// 10+1

  for (int i = 0; i < packet_size; i++) {
    byteArray[i * 4] = ((uint8_t*)&ALL_IMU[i])[0];
    byteArray[i * 4 + 1] = ((uint8_t*)&ALL_IMU[i])[1];
    byteArray[i * 4 + 2] = ((uint8_t*)&ALL_IMU[i])[2];
    byteArray[i * 4 + 3] = ((uint8_t*)&ALL_IMU[i])[3];
  }

  byteArray[packet_size * 4] = ((uint8_t*)&init_time_1)[0];
  byteArray[packet_size * 4 + 1] = ((uint8_t*)&init_time_1)[1];
  byteArray[packet_size * 4 + 2] = ((uint8_t*)&init_time_1)[2];
  byteArray[packet_size * 4 + 3] = ((uint8_t*)&init_time_1)[3];
  //    Serial.print('[');
  //
  //    Serial.print(accel_x_0); Serial.print(','); Serial.print(accel_y_0); Serial.print(','); Serial.print(accel_z_0); Serial.print(',');
  //    Serial.print(mag_x_0); Serial.print(','); Serial.print(mag_y_0); Serial.print(','); Serial.print(mag_z_0); Serial.print(',');
  //    Serial.print(gyro_x_0); Serial.print(','); Serial.print(gyro_y_0); Serial.print(','); Serial.print(gyro_z_0); Serial.print(',');
  //
  //    Serial.print(accel_x_1); Serial.print(','); Serial.print(accel_y_1); Serial.print(','); Serial.print(accel_z_1); Serial.print(',');
  //    Serial.print(mag_x_1); Serial.print(','); Serial.print(mag_y_1); Serial.print(','); Serial.print(mag_z_1); Serial.print(',');
  //    Serial.print(gyro_x_1); Serial.print(','); Serial.print(gyro_y_1); Serial.print(','); Serial.print(gyro_z_1); Serial.print(',');
  //
  //    Serial.print(accel_x_2); Serial.print(','); Serial.print(accel_y_2); Serial.print(','); Serial.print(accel_z_2); Serial.print(',');
  //    Serial.print(mag_x_2); Serial.print(','); Serial.print(mag_y_2); Serial.print(','); Serial.print(mag_z_2); Serial.print(',');
  //    Serial.print(gyro_x_2); Serial.print(','); Serial.print(gyro_y_2); Serial.print(','); Serial.print(gyro_z_1); Serial.print(',');
  //
  //    Serial.print(accel_x_3); Serial.print(','); Serial.print(accel_y_3); Serial.print(','); Serial.print(accel_z_3); Serial.print(',');
  //    Serial.print(mag_x_3); Serial.print(','); Serial.print(mag_y_3); Serial.print(','); Serial.print(mag_z_3); Serial.print(',');
  //    Serial.print(gyro_x_3); Serial.print(','); Serial.print(gyro_y_3); Serial.print(','); Serial.print(gyro_z_3); Serial.print(',');
  //
  //    Serial.print(accel_x_4); Serial.print(','); Serial.print(accel_y_4); Serial.print(','); Serial.print(accel_z_4); Serial.print(',');
  //    Serial.print(mag_x_4); Serial.print(','); Serial.print(mag_y_4); Serial.print(','); Serial.print(mag_z_4); Serial.print(',');
  //    Serial.print(gyro_x_4); Serial.print(','); Serial.print(gyro_y_4); Serial.print(','); Serial.print(gyro_z_4); Serial.print(',');
  //
  //    Serial.print(accel_x_5); Serial.print(','); Serial.print(accel_y_5); Serial.print(','); Serial.print(accel_z_5); Serial.print(',');
  //    Serial.print(mag_x_5); Serial.print(','); Serial.print(mag_y_5); Serial.print(','); Serial.print(mag_z_5); Serial.print(',');
  //    Serial.print(gyro_x_5); Serial.print(','); Serial.print(gyro_y_5); Serial.print(','); Serial.print(gyro_z_5); Serial.print(',');
  //    Serial.print(init_time_2);
  //
  //
  //
  //    Serial.print(']');
  //    Serial.print('\r');
  //    Serial.print('\n');
  //
  //  Serial.print("data:");
  //  Serial.println(init_time_2 - init_time_1);
  //  Serial.println();
  bleuart.write(byteArray, sizeof(byteArray));
  COUNT += 1;

}

void loop(void)
{
  if (Bluefruit.connected() && bleuart.notifyEnabled())
  {

    test_throughput();

  }
}
