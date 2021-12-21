#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU

unsigned long init_time = micros();
unsigned long init_time_comp = micros();
unsigned long init_time_gyro = micros();


ICM_20948_SPI ICM1; // If using SPI create an ICM_20948_SPI object
ICM_20948_SPI ICM2; // If using SPI create an ICM_20948_SPI object
ICM_20948_SPI ICM3; // If using SPI create an ICM_20948_SPI object
ICM_20948_SPI ICM4; // If using SPI create an ICM_20948_SPI object
ICM_20948_SPI ICM5; // If using SPI create an ICM_20948_SPI object
ICM_20948_SPI ICM6; // If using SPI create an ICM_20948_SPI object

bool INIT_IMU(ICM_20948_SPI* ICM, int CS_PIN) {

  ICM->enableDebugging(); // Uncomment this line to enable helpful debug messages on Serial

  bool initialized = false;
  while (!initialized)
  {
    ICM->begin(CS_PIN, SPI);
    ICM->startupDefault(false);
    Serial.print("Init ICM-");
    Serial.print(CS_PIN);

    Serial.print(F(" "));
    Serial.print(ICM->statusString());
    if (ICM->status != ICM_20948_Stat_Ok)
    {
      Serial.println(F(" Trying again..."));
      delay(500);
    }
    else
    {
      initialized = true;
    }
  }

  bool success = true; // Use success to show if the DMP configuration was successful

  success &= (ICM->initializeDMP() == ICM_20948_Stat_Ok) &
             (ICM->enableDMPSensor(INV_ICM20948_SENSOR_RAW_GYROSCOPE) == ICM_20948_Stat_Ok) &
             (ICM->enableDMPSensor(INV_ICM20948_SENSOR_RAW_ACCELEROMETER) == ICM_20948_Stat_Ok) &
             (ICM->enableDMPSensor(INV_ICM20948_SENSOR_MAGNETIC_FIELD_UNCALIBRATED) == ICM_20948_Stat_Ok) &
             (ICM->setDMPODRrate(DMP_ODR_Reg_Accel, 0) == ICM_20948_Stat_Ok) &
             (ICM->setDMPODRrate(DMP_ODR_Reg_Gyro, 0) == ICM_20948_Stat_Ok) &
             (ICM->setDMPODRrate(DMP_ODR_Reg_Cpass, 0) == ICM_20948_Stat_Ok) &
             (ICM->enableFIFO() == ICM_20948_Stat_Ok) &
             (ICM->enableDMP() == ICM_20948_Stat_Ok) &
             (ICM->resetDMP() == ICM_20948_Stat_Ok) &
             (ICM->resetFIFO() == ICM_20948_Stat_Ok);


  // Check success
  if (success)
  {
    Serial.println(F(" DMP enabled!"));
    return true;
  }
  else
  {
    Serial.println(F("Enable DMP failed!"));
    Serial.println(F("Please check that you have uncommented line 29 (#define ICM_20948_USE_DMP) in ICM_20948_C.h..."));
    return false;
  }
}


void setup()
{

  Serial.begin(115200); // Start the serial console
  Serial.println(F("ICM-20948 Example"));

  delay(100);


  while (Serial.available()) // Make sure the serial RX buffer is empty
    Serial.read();

  Serial.println(F("Press any key to continue..."));

  while (!Serial.available()) // Wait for the user to press a key (send any serial character)
    ;


  SPI.begin();
  SPI.beginTransaction(SPISettings(7000000, MSBFIRST, SPI_MODE0));
  INIT_IMU(&ICM1, 2);
  INIT_IMU(&ICM2, 3);
  INIT_IMU(&ICM3, 4);
  //  INIT_IMU(&ICM2, 5);
  //  INIT_IMU(&ICM1, 8);
  //  INIT_IMU(&ICM2, 9);
}

void print_imu_data(ICM_20948_SPI ICM, icm_20948_DMP_data_t ICM_Data) {
  if ((ICM.status == ICM_20948_Stat_Ok) || (ICM.status == ICM_20948_Stat_FIFOMoreDataAvail)) // Was valid data available?
  {

    if ( ((ICM_Data.header & DMP_header_bitmap_Compass) > 0) &
         ((ICM_Data.header & DMP_header_bitmap_Accel) > 0) &
         ((ICM_Data.header & DMP_header_bitmap_Gyro) > 0 )) // Check for Compass
    {
      float x_comp = (float)ICM_Data.Compass.Data.X; // Extract the compass data
      float y_comp = (float)ICM_Data.Compass.Data.Y;
      float z_comp = (float)ICM_Data.Compass.Data.Z;

      float x_accel = (float)ICM_Data.Raw_Accel.Data.X; // Extract the raw accelerometer data
      float y_accel = (float)ICM_Data.Raw_Accel.Data.Y;
      float z_accel = (float)ICM_Data.Raw_Accel.Data.Z;

      float x_gyro = (float)ICM_Data.Raw_Gyro.Data.X; // Extract the raw gyro data
      float y_gyro = (float)ICM_Data.Raw_Gyro.Data.Y;
      float z_gyro = (float)ICM_Data.Raw_Gyro.Data.Z;

      Serial.print(F("Compass: X:"));
      //      Serial.print(x_comp);
      //      Serial.print(F(" Y:"));
      //      Serial.print(y_comp);
      //      Serial.print(F(" Z:"));
      //      Serial.print(z_comp);
      //
      //      Serial.print(F(" Accel: X:"));
      //      Serial.print(x_accel);
      //      Serial.print(F(" Y:"));
      //      Serial.print(y_accel);
      //      Serial.print(F(" Z:"));
      //      Serial.print(z_accel);
      //
      //      Serial.print(F(" Gyro: X:"));
      //      Serial.print(x_gyro);
      //      Serial.print(F(" Y:"));
      //      Serial.print(y_gyro);
      //      Serial.print(F(" Z:"));
      Serial.println(z_gyro);



    }

    if (ICM.status != ICM_20948_Stat_FIFOMoreDataAvail) // If more data is available then we should read it right away - and not delay
    {
      delay(1); // Keep this short!
    }
  }

}

bool check_imu_ready(ICM_20948_SPI ICM, icm_20948_DMP_data_t ICM_Data) {

  if ((ICM.status == ICM_20948_Stat_Ok) || (ICM.status == ICM_20948_Stat_FIFOMoreDataAvail)) // Was valid data available?
  {

    if ( ((ICM_Data.header & DMP_header_bitmap_Compass) > 0) &
         ((ICM_Data.header & DMP_header_bitmap_Accel) > 0) &
         ((ICM_Data.header & DMP_header_bitmap_Gyro) > 0 )) // Check for Compass
    {
      return true;
    }
  }
  return false;
}


bool check_all_imu_ready( icm_20948_DMP_data_t ICM_Data[]) {
  bool success = true;

  //  success &= check_imu_ready(ICM1, ICM_Data[0]);
  success &= check_imu_ready(ICM2, ICM_Data[1]);


  return success;
}

void loop()
{
//  icm_20948_DMP_data_t data_1;
//  ICM1.readDMPdataFromFIFO(&data_1);
//
//  icm_20948_DMP_data_t data_2;
//  ICM2.readDMPdataFromFIFO(&data_2);
//
//  icm_20948_DMP_data_t ICM_Data[2] = {data_1, data_2};
//
//  if (check_all_imu_ready(ICM_Data)) {
//
//    //    Serial.print("ICM_1: ");
//    //    print_imu_data(ICM1, data_1);
//    Serial.print("ICM_2: ");
//    print_imu_data(ICM2, data_2);
//    //    Serial.println();
//
//    Serial.print("diff comp:");
//    Serial.println(micros() - init_time);
//    init_time = micros();
//  }

}

// initializeDMP is a weak function. Let's overwrite it so we can increase the sample rate
ICM_20948_Status_e ICM_20948::initializeDMP(void)
{
  // The ICM-20948 is awake and ready but hasn't been configured. Let's step through the configuration
  // sequence from InvenSense's _confidential_ Application Note "Programming Sequence for DMP Hardware Functions".

  ICM_20948_Status_e  result = ICM_20948_Stat_Ok; // Use result and worstResult to show if the configuration was successful
  ICM_20948_Status_e  worstResult = ICM_20948_Stat_Ok;

  result = i2cControllerConfigurePeripheral(0, MAG_AK09916_I2C_ADDR, AK09916_REG_RSV2, 10, true, true, false, true, true); if (result > worstResult) worstResult = result;

  result = i2cControllerConfigurePeripheral(1, MAG_AK09916_I2C_ADDR, AK09916_REG_CNTL2, 1, false, true, false, false, false, AK09916_mode_single); if (result > worstResult) worstResult = result;

  result = setBank(3); if (result > worstResult) worstResult = result; // Select Bank 3
  uint8_t mstODRconfig = 0x04; // Set the ODR configuration to 1100/2^4 = 68.75Hz
  result = write(AGB3_REG_I2C_MST_ODR_CONFIG, &mstODRconfig, 1); if (result > worstResult) worstResult = result; // Write one byte to the I2C_MST_ODR_CONFIG register


  result = setClockSource(ICM_20948_Clock_Auto); if (result > worstResult) worstResult = result; // This is shorthand: success will be set to false if setClockSource fails


  result = setBank(0); if (result > worstResult) worstResult = result;                               // Select Bank 0
  uint8_t pwrMgmt2 = 0x40;                                                          // Set the reserved bit 6 (pressure sensor disable?)
  result = write(AGB0_REG_PWR_MGMT_2, &pwrMgmt2, 1); if (result > worstResult) worstResult = result; // Write one byte to the PWR_MGMT_2 register


  result = setSampleMode(ICM_20948_Internal_Mst, ICM_20948_Sample_Mode_Cycled); if (result > worstResult) worstResult = result;

  // Disable the FIFO
  result = enableFIFO(false); if (result > worstResult) worstResult = result;

  // Disable the DMP
  result = enableDMP(false); if (result > worstResult) worstResult = result;


  ICM_20948_fss_t myFSS; // This uses a "Full Scale Settings" structure that can contain values for all configurable sensors
  myFSS.a = gpm4;        // (ICM_20948_ACCEL_CONFIG_FS_SEL_e)

  myFSS.g = dps2000;     // (ICM_20948_GYRO_CONFIG_1_FS_SEL_e)

  result = setFullScale((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS); if (result > worstResult) worstResult = result;


  result = enableDLPF(ICM_20948_Internal_Gyr, true); if (result > worstResult) worstResult = result;


  result = setBank(0); if (result > worstResult) worstResult = result; // Select Bank 0
  uint8_t zero = 0;
  result = write(AGB0_REG_FIFO_EN_1, &zero, 1); if (result > worstResult) worstResult = result;

  result = write(AGB0_REG_FIFO_EN_2, &zero, 1); if (result > worstResult) worstResult = result;


  result = intEnableRawDataReady(false); if (result > worstResult) worstResult = result;


  result = resetFIFO(); if (result > worstResult) worstResult = result;


  ICM_20948_smplrt_t mySmplrt;
  //  mySmplrt.g = 19; // ODR is computed as follows: 1.1 kHz/(1+GYRO_SMPLRT_DIV[7:0]). 19 = 55Hz. InvenSense Nucleo example uses 19 (0x13).
  //  mySmplrt.a = 19; // ODR is computed as follows: 1.125 kHz/(1+ACCEL_SMPLRT_DIV[11:0]). 19 = 56.25Hz. InvenSense Nucleo example uses 19 (0x13).
  mySmplrt.g = 4; // 225Hz
  mySmplrt.a = 4; // 225Hz
  //mySmplrt.g = 8; // 112Hz
  //mySmplrt.a = 8; // 112Hz
  result = setSampleRate((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), mySmplrt); if (result > worstResult) worstResult = result;


  result = setDMPstartAddress(); if (result > worstResult) worstResult = result; // Defaults to DMP_START_ADDRESS


  result = loadDMPFirmware(); if (result > worstResult) worstResult = result;


  result = setDMPstartAddress(); if (result > worstResult) worstResult = result; // Defaults to DMP_START_ADDRESS


  result = setBank(0); if (result > worstResult) worstResult = result; // Select Bank 0
  uint8_t fix = 0x48;
  result = write(AGB0_REG_HW_FIX_DISABLE, &fix, 1); if (result > worstResult) worstResult = result;


  result = setBank(0); if (result > worstResult) worstResult = result; // Select Bank 0
  uint8_t fifoPrio = 0xE4;
  result = write(AGB0_REG_SINGLE_FIFO_PRIORITY_SEL, &fifoPrio, 1); if (result > worstResult) worstResult = result;


  const unsigned char accScale[4] = {0x04, 0x00, 0x00, 0x00};
  result = writeDMPmems(ACC_SCALE, 4, &accScale[0]); if (result > worstResult) worstResult = result; // Write accScale to ACC_SCALE DMP register

  const unsigned char accScale2[4] = {0x00, 0x04, 0x00, 0x00};
  result = writeDMPmems(ACC_SCALE2, 4, &accScale2[0]); if (result > worstResult) worstResult = result; // Write accScale2 to ACC_SCALE2 DMP register


  const unsigned char mountMultiplierZero[4] = {0x00, 0x00, 0x00, 0x00};
  const unsigned char mountMultiplierPlus[4] = {0x09, 0x99, 0x99, 0x99};  // Value taken from InvenSense Nucleo example
  const unsigned char mountMultiplierMinus[4] = {0xF6, 0x66, 0x66, 0x67}; // Value taken from InvenSense Nucleo example
  result = writeDMPmems(CPASS_MTX_00, 4, &mountMultiplierPlus[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_01, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_02, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_10, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_11, 4, &mountMultiplierMinus[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_12, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_20, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_21, 4, &mountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(CPASS_MTX_22, 4, &mountMultiplierMinus[0]); if (result > worstResult) worstResult = result;

  // Configure the B2S Mounting Matrix
  const unsigned char b2sMountMultiplierZero[4] = {0x00, 0x00, 0x00, 0x00};
  const unsigned char b2sMountMultiplierPlus[4] = {0x40, 0x00, 0x00, 0x00}; // Value taken from InvenSense Nucleo example
  result = writeDMPmems(B2S_MTX_00, 4, &b2sMountMultiplierPlus[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_01, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_02, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_10, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_11, 4, &b2sMountMultiplierPlus[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_12, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_20, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_21, 4, &b2sMountMultiplierZero[0]); if (result > worstResult) worstResult = result;
  result = writeDMPmems(B2S_MTX_22, 4, &b2sMountMultiplierPlus[0]); if (result > worstResult) worstResult = result;


  result = setGyroSF(4, 3); if (result > worstResult) worstResult = result; // 4 = 225Hz (see above), 3 = 2000dps (see above)


  const unsigned char gyroFullScale[4] = {0x10, 0x00, 0x00, 0x00}; // 2000dps : 2^28
  result = writeDMPmems(GYRO_FULLSCALE, 4, &gyroFullScale[0]); if (result > worstResult) worstResult = result;

  // Configure the Accel Only Gain: 15252014 (225Hz) 30504029 (112Hz) 61117001 (56Hz)
  //const unsigned char accelOnlyGain[4] = {0x03, 0xA4, 0x92, 0x49}; // 56Hz
  const unsigned char accelOnlyGain[4] = {0x00, 0xE8, 0xBA, 0x2E}; // 225Hz
  //const unsigned char accelOnlyGain[4] = {0x01, 0xD1, 0x74, 0x5D}; // 112Hz
  result = writeDMPmems(ACCEL_ONLY_GAIN, 4, &accelOnlyGain[0]); if (result > worstResult) worstResult = result;

  // Configure the Accel Alpha Var: 1026019965 (225Hz) 977872018 (112Hz) 882002213 (56Hz)
  //const unsigned char accelAlphaVar[4] = {0x34, 0x92, 0x49, 0x25}; // 56Hz
  const unsigned char accelAlphaVar[4] = {0x3D, 0x27, 0xD2, 0x7D}; // 225Hz
  //const unsigned char accelAlphaVar[4] = {0x3A, 0x49, 0x24, 0x92}; // 112Hz
  result = writeDMPmems(ACCEL_ALPHA_VAR, 4, &accelAlphaVar[0]); if (result > worstResult) worstResult = result;

  // Configure the Accel A Var: 47721859 (225Hz) 95869806 (112Hz) 191739611 (56Hz)
  //const unsigned char accelAVar[4] = {0x0B, 0x6D, 0xB6, 0xDB}; // 56Hz
  const unsigned char accelAVar[4] = {0x02, 0xD8, 0x2D, 0x83}; // 225Hz
  //const unsigned char accelAVar[4] = {0x05, 0xB6, 0xDB, 0x6E}; // 112Hz
  result = writeDMPmems(ACCEL_A_VAR, 4, &accelAVar[0]); if (result > worstResult) worstResult = result;

  // Configure the Accel Cal Rate
  const unsigned char accelCalRate[4] = {0x00, 0x00}; // Value taken from InvenSense Nucleo example
  result = writeDMPmems(ACCEL_CAL_RATE, 2, &accelCalRate[0]); if (result > worstResult) worstResult = result;

  // Configure the Compass Time Buffer. The I2C Master ODR Configuration (see above) sets the magnetometer read rate to 68.75Hz.
  // Let's set the Compass Time Buffer to 69 (Hz).
  const unsigned char compassRate[2] = {0x00, 0x45}; // 69Hz
  result = writeDMPmems(CPASS_TIME_BUFFER, 2, &compassRate[0]); if (result > worstResult) worstResult = result;

  // Enable DMP interrupt
  // This would be the most efficient way of getting the DMP data, instead of polling the FIFO
  //result = intEnableDMP(true); if (result > worstResult) worstResult = result;

  return worstResult;
}
