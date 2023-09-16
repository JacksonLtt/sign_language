/*
    Video: https://www.youtube.com/watch?v=oCMOYS71NIU
    Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleNotify.cpp
    Ported to Arduino ESP32 by Evandro Copercini

   Create a BLE server that, once we receive a connection, will send periodic notifications.
   The service advertises itself as: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
   Has a characteristic of: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E - used for receiving data with "WRITE"
   Has a characteristic of: 6E400003-B5A3-F393-E0A9-E50E24DCCA9E - used to send data with  "NOTIFY"

   The design of creating the BLE server is:
   1. Create a BLE Server
   2. Create a BLE Service
   3. Create a BLE Characteristic on the Service
   4. Create a BLE Descriptor on the characteristic
   5. Start the service.
   6. Start advertising.

   In this example rxValue is the data received (only accessible inside that function).
   And txValue is the data to be sent, in this example just a byte incremented every second.
*/
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;

int count = 0;
int send_request = 0;

// ICM20948
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_ICM20948 icm1, icm2;


// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


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

        Serial.print("Received Value: ");

        Serial.println(rxValue[0]);
        uint8_t ch;
        ch = (uint8_t) rxValue[0];
        if ( ch == (uint8_t)'s' or ch == (uint8_t)'r' or ch == (uint8_t)'t' or ch == (uint8_t)'c') {
          send_request = 1;
          count = 0;

        }
        else if (ch == (uint8_t)'e') {
          send_request = 0;
        }
      }
    }
};


void setup() {
  Serial.begin(115200);


  // SETUP icm20948

  if (!icm1.begin_I2C(0x69)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }


  //  Serial.println(icm.ICM20948_I2CADDR_DEFAULT);
  icm1.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm1.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm1.setMagDataRate(AK09916_MAG_DATARATE_100_HZ); // setting magnetometer 100 Hz
  Serial.println("Right IMU Found!");


  if (!icm2.begin_I2C(0x68)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }


  //  Serial.println(icm.ICM20948_I2CADDR_DEFAULT);
  icm2.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm2.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm2.setMagDataRate(AK09916_MAG_DATARATE_100_HZ); // setting magnetometer 100 Hz
  Serial.println("Left IMU Found!");

  // Create the BLE Device
  BLEDevice::init("ear#1");

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
  Serial.println("ear#1");
  Serial.println("Waiting a client connection to notify...");
}

void loop() {

  if (deviceConnected && send_request == 1) {
    float start_time = micros();



    //retrive data
    sensors_event_t accel1;
    sensors_event_t gyro1;
    sensors_event_t mag1;
    sensors_event_t temp1;
    icm1.getEvent(&accel1, &gyro1, &temp1, &mag1);

    sensors_event_t accel2;
    sensors_event_t gyro2;
    sensors_event_t mag2;
    sensors_event_t temp2;
    icm2.getEvent(&accel2, &gyro2, &temp2, &mag2);
    float IMU_1[] = {accel1.acceleration.x, accel1.acceleration.y, accel1.acceleration.z, // acceleration is measured in m/s^2
                     mag1.magnetic.x, mag1.magnetic.y, mag1.magnetic.z, // magnetometer is measured in uT
                     gyro1.gyro.x, gyro1.gyro.y, gyro1.gyro.z,
                     accel2.acceleration.x, accel2.acceleration.y, accel2.acceleration.z, // acceleration is measured in m/s^2
                     mag2.magnetic.x, mag2.magnetic.y, mag2.magnetic.z, // magnetometer is measured in uT
                     gyro2.gyro.x, gyro2.gyro.y, gyro2.gyro.z,
                     start_time
                    }; // gyro is measured in radians/s

    //    Serial.print("IMU data:");
    //    for (int i = 0; i < 9; i++) {
    //
    //      Serial.print(IMU_1[i]);
    //      Serial.print(",");
    //
    //    }
    //    Serial.print(start_time);
    //    Serial.println();

    //data process

    int packet_size = 19;
    int total_size = packet_size * 4;
    byte byteArray[total_size];// 10+1

    for (int i = 0; i < 19; i++) {
      byteArray[i * 4] = ((uint8_t*)&IMU_1[i])[0];
      byteArray[i * 4 + 1] = ((uint8_t*)&IMU_1[i])[1];
      byteArray[i * 4 + 2] = ((uint8_t*)&IMU_1[i])[2];
      byteArray[i * 4 + 3] = ((uint8_t*)&IMU_1[i])[3];
    }


    // send data
    pTxCharacteristic->setValue(byteArray, total_size);
    pTxCharacteristic->notify();
    unsigned long timm_g = micros() - start_time;

    count += 1;
    Serial.println(count);
    delay(4); // bluetooth stack will go into congestion, if too many packets are sent
  }


  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500); // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising(); // restart advertising
    Serial.println("start advertising");
    count = 0;
    oldDeviceConnected = deviceConnected;
    send_request = 0;
  }

  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = deviceConnected;
  }
}
