/*
  9/1/2021 Integrate five IMU together by 4 I2C bus by using multiplexer offline and 1 I2C
  9/5/2021 Five IMU together by using multiplexer
  9/23/2021 Six IMU by using multplexer
  11/2/2021 six IMU data, sent via BLE
  12/6/2021 testing two device, sent via BLE THIS IS right HAND
*/

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
#define I2C_SDA_1 21
#define I2C_SCL_1 22


TwoWire I2CICM_1 = TwoWire(0);

//BLE Lib
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;


// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


// Liraries for Json
#include "ArduinoJson.h"
unsigned long init_time_1;
unsigned long init_time_2;

unsigned long id = 1;
int count = 0;

// Library for BLE
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      std::string rxValue = pCharacteristic->getValue();

      if (rxValue.length() > 0) {
        Serial.println("*********");
        Serial.print("Received Value: ");
        for (int i = 0; i < rxValue.length(); i++)
          Serial.print(rxValue[i]);

        Serial.println();
        Serial.println("*********");
      }
    }
};



void setup()
{
  Serial.begin(115200);
  Serial.println("Qwiic Mux Shield Read Example");
  I2CICM_1.begin(I2C_SDA_1, I2C_SCL_1, 3400000);
  Wire.begin();

  //Create set of pointers to the class
  ICM20948_Sensor = new Adafruit_ICM20948 *[NUMBER_OF_SENSORS];

  //Assign pointers to instances of the class
  for (int x = 0; x < NUMBER_OF_SENSORS; x++)
    ICM20948_Sensor[x] = new Adafruit_ICM20948();

  if (myMux.begin(0x70, I2CICM_1) == false)
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
  if (!ICM20948_Sensor[0]->begin_I2C(0X69, &I2CICM_1)) //Begin returns 0 on a good init
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

  if (!ICM20948_Sensor[1]->begin_I2C(0X68, &I2CICM_1)) //Begin returns 0 on a good init
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
  if (!ICM20948_Sensor[2]->begin_I2C(0X68, &I2CICM_1)) //Begin returns 0 on a good init
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

  if (!ICM20948_Sensor[3]->begin_I2C(0X69, &I2CICM_1)) //Begin returns 0 on a good init
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
  if (!ICM20948_Sensor[4]->begin_I2C(0X68, &I2CICM_1)) //Begin returns 0 on a good init
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

  if (!ICM20948_Sensor[5]->begin_I2C(0X69, &I2CICM_1)) //Begin returns 0 on a good init
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

  // Create the BLE Device
  BLEDevice::init("Right hand");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pTxCharacteristic = pService->createCharacteristic(
                        CHARACTERISTIC_UUID_TX,
                        BLECharacteristic::PROPERTY_NOTIFY
                      );

  pTxCharacteristic->addDescriptor(new BLE2902());

  BLECharacteristic * pRxCharacteristic = pService->createCharacteristic(
      CHARACTERISTIC_UUID_RX,
      BLECharacteristic::PROPERTY_WRITE
                                          );

  pRxCharacteristic->setCallbacks(new MyCallbacks());

  // Start the service
  pService->start();

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");

}


void print_array(float Array[], int size_of_Array) {
  Serial.print("[");
  for (int i = 0; i < size_of_Array; i++)
  {
    Serial.print(Array[i]);
    Serial.print(",");
  }
  Serial.println("]");
}


void get_icm_data(Adafruit_ICM20948* icm, String ICM_Name) {
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t mag;
  sensors_event_t temp;
  icm->getEvent(&accel, &gyro, &temp, &mag);

  float accel_x = accel.acceleration.x;
  float accel_y = accel.acceleration.y;
  float accel_z = accel.acceleration.z;

  float mag_x = mag.magnetic.x;
  float mag_y = mag.magnetic.y;
  float mag_z = mag.magnetic.z;

  float gyro_x = gyro.gyro.x;
  float gyro_y = gyro.gyro.y;
  float gyro_z = gyro.gyro.z;


  float IMU_1[] = {accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z};


  Serial.print(ICM_Name);
  print_array(IMU_1, 9);
}

void loop()
{


  if (deviceConnected) {
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


//    Serial.print('[');
//
//    Serial.print(accel_x_0); Serial.print(','); Serial.print(accel_y_0); Serial.print(','); Serial.print(accel_z_0); Serial.print(',');
//    Serial.print(mag_x_0); Serial.print(','); Serial.print(mag_y_0); Serial.print(','); Serial.print(mag_z_0); Serial.print(',');
//    Serial.print(gyro_x_0); Serial.print(','); Serial.print(gyro_y_0); Serial.print(','); Serial.print(gyro_z_0); Serial.print(',');
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
//    Serial.print(init_time_1);Serial.print(','); Serial.print(id); 
//
//
//
//    Serial.print(']');
//    Serial.print('\r');
//    Serial.print('\n');



    // process data
    int packet_size = 54;
    int total_size = (packet_size + 2) * 4;
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

    byteArray[packet_size * 4 + 4] = ((uint8_t*)&id)[0];
    byteArray[packet_size * 4 + 5] = ((uint8_t*)&id)[1];
    byteArray[packet_size * 4 + 6] = ((uint8_t*)&id)[2];
    byteArray[packet_size * 4 + 7] = ((uint8_t*)&id)[3];

    // send data
    pTxCharacteristic->setValue(byteArray, total_size);
    pTxCharacteristic->notify();
    init_time_2 = micros();

    Serial.print("data:");
    count+=1;
    Serial.println(count);

    delay(10);
  }
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
    count = 0;
  }

  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = deviceConnected;
  }







  //  Serial.println();

}
