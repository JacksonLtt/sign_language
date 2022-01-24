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


void update_imu(ICM_20948_SPI *sensor, int index) {
  //  Serial.print("begin ");
  //  Serial.println(name_imu[index]);
  unsigned long init_time = micros();
  if (sensor->dataReady())
  {
    sensor->getAGMT();         // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    printScaledAGMT(sensor); // This function takes into account the scale settings from when the measurement was made to calculate the values with units
    getScaledAGMT(sensor);
    //    delay(1);
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
  unsigned long init_time = micros();
  update_imu(ICM20948_Sensor[0], 0);
  update_imu(ICM20948_Sensor[1], 1);
  update_imu(ICM20948_Sensor[2], 2);
  update_imu(ICM20948_Sensor[3], 3);
  update_imu(ICM20948_Sensor[4], 4);
  delay(1000);
  Serial.print("diff: ");
  Serial.println(micros() - init_time);
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
