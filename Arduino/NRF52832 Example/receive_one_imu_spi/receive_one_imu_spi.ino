/*
  8/27/2021 get one IMU together by 1 SPI
*/
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_ICM20948 icm;
uint16_t measurement_delay_us = 65535; // Delay between measurements for testing
// For SPI mode, we need a CS pin
#define ICM_CS 18
// For software-SPI mode we need SCK/MOSI/MISO pins
#define ICM_SCK 14
#define ICM_MISO 15
#define ICM_MOSI 13

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit ICM20948 test!");

  // Try to initialize!
  //  if (!icm.begin_I2C()) {
  if (!icm.begin_SPI(ICM_CS)) {
    //  if (!icm.begin_SPI(ICM_CS, ICM_SCK, ICM_MISO, ICM_MOSI)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("ICM20948 Found!");
  icm.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm.setMagDataRate(AK09916_MAG_DATARATE_50_HZ); // setting magnetometer 100 Hz

}

void loop() {

  //  /* Get a new normalized sensor event */
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t magn;
  sensors_event_t temp;
  icm.getEvent(&accel, &gyro, &temp, &magn);

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("\t\tAccel X: ");
  Serial.print(accel.acceleration.x);
  Serial.print(" \tY: ");
  Serial.print(accel.acceleration.y);
  Serial.print(" \tZ: ");
  Serial.print(accel.acceleration.z);
  Serial.println(" m/s^2 ");

  Serial.print("\t\tMag X: ");
  Serial.print(magn.magnetic.x);
  Serial.print(" \tY: ");
  Serial.print(magn.magnetic.y);
  Serial.print(" \tZ: ");
  Serial.print(magn.magnetic.z);
  Serial.println(" uT");

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("\t\tGyro X: ");
  Serial.print(gyro.gyro.x);
  Serial.print(" \tY: ");
  Serial.print(gyro.gyro.y);
  Serial.print(" \tZ: ");
  Serial.print(gyro.gyro.z);
  Serial.println(" radians/s ");
  Serial.println();

  delay(1000);
}
