/*
  8/27/2021 get one IMU together by 1 SPI
*/
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_ICM20948 icm1;

Adafruit_ICM20948 icm2;

Adafruit_ICM20948 icm3;

uint16_t measurement_delay_us = 65535; // Delay between measurements for testing
// For SPI mode, we need a CS pin
#define ICM_CS 2


void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit ICM1 test!");

  // Try to initialize!
  if (!icm1.begin_SPI(2)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  else {
    Serial.println("ICM20948 Found!");
  }

  icm1.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm1.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm1.setMagDataRate(AK09916_MAG_DATARATE_50_HZ); // setting magnetometer 100 Hz

//  Serial.println("Adafruit ICM2 test!");
//
//  // Try to initialize!
//  if (!icm2.begin_SPI(3)) {
//
//    Serial.println("Failed to find ICM20948 chip");
//    while (1) {
//      delay(10);
//    }
//  }
//  else {
//    Serial.println("ICM20948 Found!");
//  }
//
//  icm2.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
//  icm2.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
//  icm2.setMagDataRate(AK09916_MAG_DATARATE_50_HZ); // setting magnetometer 100 Hz
//
//  Serial.println("Adafruit ICM3 test!");
//
//  // Try to initialize!
//  if (!icm3.begin_SPI(4)) {
//
//    Serial.println("Failed to find ICM20948 chip");
//    while (1) {
//      delay(10);
//    }
//  }
//  else {
//    Serial.println("ICM20948 Found!");
//  }
//  icm3.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
//  icm3.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
//  icm3.setMagDataRate(AK09916_MAG_DATARATE_50_HZ); // setting magnetometer 100 Hz
//  Serial.println("End\n");
}



void print_data(Adafruit_ICM20948 icm) {
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t magn;
  sensors_event_t temp;
  icm.getEvent(&accel, &gyro, &temp, &magn);

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.println("ICM1");
  Serial.print("\t\tAccel X: ");
  Serial.print(accel.acceleration.x);
  Serial.print(" \tY: ");
  Serial.print(accel.acceleration.y);
  Serial.print(" \tZ: ");
  Serial.print(accel.acceleration.z);
  Serial.print(" m/s^2 ");

  Serial.print("\t\tMag X: ");
  Serial.print(magn.magnetic.x);
  Serial.print(" \tY: ");
  Serial.print(magn.magnetic.y);
  Serial.print(" \tZ: ");
  Serial.print(magn.magnetic.z);
  Serial.print(" uT");

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("\t\tGyro X: ");
  Serial.print(gyro.gyro.x);
  Serial.print(" \tY: ");
  Serial.print(gyro.gyro.y);
  Serial.print(" \tZ: ");
  Serial.print(gyro.gyro.z);
  Serial.print(" radians/s ");
  Serial.println();

}
void loop() {

//  sensors_event_t accel;
//  sensors_event_t gyro;
//  sensors_event_t magn;
//  sensors_event_t temp;
//  icm1.getEvent(&accel, &gyro, &temp, &magn);
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.println("ICM1");
//  Serial.print("\t\tAccel X: ");
//  Serial.print(accel.acceleration.x);
//  Serial.print(" \tY: ");
//  Serial.print(accel.acceleration.y);
//  Serial.print(" \tZ: ");
//  Serial.print(accel.acceleration.z);
//  Serial.print(" m/s^2 ");
//
//  Serial.print("\t\tMag X: ");
//  Serial.print(magn.magnetic.x);
//  Serial.print(" \tY: ");
//  Serial.print(magn.magnetic.y);
//  Serial.print(" \tZ: ");
//  Serial.print(magn.magnetic.z);
//  Serial.print(" uT");
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print("\t\tGyro X: ");
//  Serial.print(gyro.gyro.x);
//  Serial.print(" \tY: ");
//  Serial.print(gyro.gyro.y);
//  Serial.print(" \tZ: ");
//  Serial.print(gyro.gyro.z);
//  Serial.print(" radians/s ");
//  Serial.println();
//
//
//  icm2.getEvent(&accel, &gyro, &temp, &magn);
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.println("ICM2");
//  Serial.print("\t\tAccel X: ");
//  Serial.print(accel.acceleration.x);
//  Serial.print(" \tY: ");
//  Serial.print(accel.acceleration.y);
//  Serial.print(" \tZ: ");
//  Serial.print(accel.acceleration.z);
//  Serial.print(" m/s^2 ");
//
//  Serial.print("\t\tMag X: ");
//  Serial.print(magn.magnetic.x);
//  Serial.print(" \tY: ");
//  Serial.print(magn.magnetic.y);
//  Serial.print(" \tZ: ");
//  Serial.print(magn.magnetic.z);
//  Serial.print(" uT");
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print("\t\tGyro X: ");
//  Serial.print(gyro.gyro.x);
//  Serial.print(" \tY: ");
//  Serial.print(gyro.gyro.y);
//  Serial.print(" \tZ: ");
//  Serial.print(gyro.gyro.z);
//  Serial.print(" radians/s ");
//  Serial.println();
//
//
//  icm3.getEvent(&accel, &gyro, &temp, &magn);
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.println("ICM3");
//  Serial.print("\t\tAccel X: ");
//  Serial.print(accel.acceleration.x);
//  Serial.print(" \tY: ");
//  Serial.print(accel.acceleration.y);
//  Serial.print(" \tZ: ");
//  Serial.print(accel.acceleration.z);
//  Serial.print(" m/s^2 ");
//
//  Serial.print("\t\tMag X: ");
//  Serial.print(magn.magnetic.x);
//  Serial.print(" \tY: ");
//  Serial.print(magn.magnetic.y);
//  Serial.print(" \tZ: ");
//  Serial.print(magn.magnetic.z);
//  Serial.print(" uT");
//
//  /* Display the results (acceleration is measured in m/s^2) */
//  Serial.print("\t\tGyro X: ");
//  Serial.print(gyro.gyro.x);
//  Serial.print(" \tY: ");
//  Serial.print(gyro.gyro.y);
//  Serial.print(" \tZ: ");
//  Serial.print(gyro.gyro.z);
//  Serial.print(" radians/s ");
//  Serial.println();
//
//  delay(1);
}
