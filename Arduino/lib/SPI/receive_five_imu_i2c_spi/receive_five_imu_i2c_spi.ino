/* 
  8/27/2021 Integrate five IMU together by 2 I2C bus and 1 SPI
  */ 

// Libraries for ICM 20948
#include <Adafruit_ICM20X.h>
#include <Adafruit_ICM20948.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_ICM20948 icm_1;
Adafruit_ICM20948 icm_2;
Adafruit_ICM20948 icm_3;
Adafruit_ICM20948 icm_4;
Adafruit_ICM20948 icm_5;

/* I2C_SDA, I2C_SCL
  (33,32) I2C bus for icm_1 & icm_2 
  (33,32) I2C bus for icm_1 & icm_2 
 */
#define I2C_SDA_1 21
#define I2C_SCL_1 22 
#define I2C_SDA_2 33
#define I2C_SCL_2 32
TwoWire I2CICM_1 = TwoWire(0);
TwoWire I2CICM_2 = TwoWire(1);


/*
  For software-SPI mode we need SCK (SCL)/MOSI (SDA)/MISO (SDO)/CS (SS) pins
 */
#define ICM_CS 27
#define ICM_SCK 18
#define ICM_MISO 19
#define ICM_MOSI 23


// Liraries for Json
#include "ArduinoJson.h"


// initialize icm by i2c
void initialize_icm_by_i2c(uint8_t i2c_address,Adafruit_ICM20948* icm,TwoWire *I2CICM,int I2C_SDA,int I2C_SCL,String ICM_Name){
    // Try to initialize!
  if (!icm->begin_I2C(i2c_address,I2CICM)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.print(ICM_Name);
  Serial.println(" Found!");
  icm->setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm->setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); // setting magnetometer 100 Hz
}

void initialize_icm_by_spi(Adafruit_ICM20948* icm,int SPI_CS,int SPI_SCK,int SPI_MISO,int SPI_MOSI,String ICM_Name){
    // Try to initialize!
  if (!icm->begin_SPI(SPI_CS, SPI_SCK, SPI_MISO, SPI_MOSI)) {

    Serial.println("Failed to find ICM20948 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.print(ICM_Name);
  Serial.println(" Found!");
  icm->setAccelRange(ICM20948_ACCEL_RANGE_16_G); // setting accelorator +-16G, data rate: 1125/(1+accel_divisor), accel_divisor = 20
  icm->setGyroRange(ICM20948_GYRO_RANGE_250_DPS); // setting gyro 250 DPS, data rate: 1100 / (1+gyro_divisor), gyro_divisor = 10
  icm->setMagDataRate(AK09916_MAG_DATARATE_100_HZ); // setting magnetometer 100 Hz
}

void setup(void) {
  Serial.begin(115200);
  I2CICM_1.begin(I2C_SDA_1,I2C_SCL_1,1000000);
  I2CICM_2.begin(I2C_SDA_2,I2C_SCL_2,1000000);
  initialize_icm_by_i2c(0x68, &icm_1, &I2CICM_1,I2C_SDA_1,I2C_SCL_1, "ICM_1");
  initialize_icm_by_i2c(0x69, &icm_2, &I2CICM_1,I2C_SDA_1,I2C_SCL_1, "ICM_2");
  initialize_icm_by_i2c(0x68, &icm_3, &I2CICM_2,I2C_SDA_2,I2C_SCL_2, "ICM_3");
  initialize_icm_by_i2c(0x69, &icm_4, &I2CICM_2,I2C_SDA_2,I2C_SCL_2, "ICM_4");
  initialize_icm_by_spi(&icm_5, ICM_CS, ICM_SCK, ICM_MISO, ICM_MOSI, "ICM_5");
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

void print_array(float Array[],int size_of_Array){
  Serial.print("[");
    for(int i = 0; i < size_of_Array; i++)
  {
    Serial.print(Array[i]);
    Serial.print(",");
  }
  Serial.println("]");
}


void get_icm_data(Adafruit_ICM20948* icm,String ICM_Name){
  sensors_event_t accel;
  sensors_event_t gyro;
  sensors_event_t magn;
  sensors_event_t temp;
  icm->getEvent(&accel, &gyro, &temp, &magn);

  float accel_x = accel.acceleration.x;
  float accel_y = accel.acceleration.y;
  float accel_z = accel.acceleration.z;
  
  float mag_x = magn.magnetic.x;
  float mag_y = magn.magnetic.y;
  float mag_z = magn.magnetic.z;

  float gyro_x = gyro.gyro.x;
  float gyro_y = gyro.gyro.y;
  float gyro_z = gyro.gyro.z;

  
  float IMU_1[] = {accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,mag_x,mag_y,mag_z};


  Serial.print(ICM_Name);
  print_array(IMU_1,9);
}

<<<<<<< HEAD
=======
void merge_five_data(float imu_1[], float, imu_2[], float imu_3[], float imu_4[],float imu_5[], float &imu_6){

  for(int i = 0; i < 9; i++)
  {
      imu_6[]
  }
}
>>>>>>> 2c49861ca80f3fc22cf44801839293ff4e1cadae

void loop() {

  //  /* Get a new normalized sensor event */
  get_icm_data(&icm_1,"ICM_1");
  get_icm_data(&icm_2,"ICM_2");
  get_icm_data(&icm_3,"ICM_3");
  get_icm_data(&icm_4,"ICM_4");
  get_icm_data(&icm_5,"ICM_5");
  Serial.println();
  delay(1000);
}
