// 8/25/2021 Collect 9DoF from one ICM 20948
// 8/26/2021 Simplify 9DoF collected from one ICM 20948, offline

// Libraries for ICM 20948
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_ICM20948 icm;

// Liraries for Json
#include "ArduinoJson.h"


void setup(void) {
  Serial.begin(115200);

  Serial.println("Adafruit ICM20948 test!");

  // Try to initialize!
  uint8_t new_addr = 0x69;
  if (!icm.begin_I2C(new_addr)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("ICM20948 Found!");
  
//  Serial.println(icm.ICM20948_I2CADDR_DEFAULT);
  icm.setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm.setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm.setMagDataRate(AK09916_MAG_DATARATE_100_HZ); // setting magnetometer 100 Hz

}

void generate_array_from_int_array(float imu_array[], int size_of_array,JsonArray& all_imu){

    for (int i = 0; i< size_of_array;i++){
        all_imu.add(imu_array[i]);
    }

    String str_data;
    serializeJson(all_imu, str_data);
    Serial.print("Sample data: ");
    Serial.println(str_data);
}


void loop() {

  //  /* Get a new normalized sensor event */
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t mag;
  sensors_event_t temp;
  icm.getEvent(&accel, &gyro, &temp, &mag);

  float IMU_1[] = {accel.acceleration.x,accel.acceleration.y,accel.acceleration.z, // acceleration is measured in m/s^2
                   mag.magnetic.x,mag.magnetic.y,mag.magnetic.z, // magnetometer is measured in uT
                   gyro.gyro.x,gyro.gyro.y,gyro.gyro.z}; // gyro is measured in radians/s
  
  StaticJsonDocument<400> message_load;
  // create an empty array
  JsonArray all_imu = message_load.to<JsonArray>();
  generate_array_from_int_array(IMU_1,9,all_imu);

  delay(1000);
}
