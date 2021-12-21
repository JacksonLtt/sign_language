/*
  Battery Monitor

  This example creates a BLE peripheral with the standard battery service and
  level characteristic. The A0 pin is used to calculate the battery level.

  The circuit:
  - Arduino MKR WiFi 1010, Arduino Uno WiFi Rev2 board, Arduino Nano 33 IoT,
    Arduino Nano 33 BLE, or Arduino Nano 33 BLE Sense board.

  You can use a generic BLE central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>

// BLE Battery Service
//BLEService batteryService("180F");
BLEService batteryService("6E400001-B5A3-F393-E0A9-E50E24DCCA9E");

// BLE Battery Level Characteristic
BLECharacteristic batteryLevelChar("6E400003-B5A3-F393-E0A9-E50E24DCCA9E",  // standard 16-bit characteristic UUID
                                   BLERead | BLENotify, 220, true); // remote clients will be able to get notifications if this characteristic changes

int oldBatteryLevel = 0;  // last battery level reading from analog input
long previousMillis = 0;  // last time the battery level was checked, in ms

int count = 0;
void setup() {
  Serial.begin(9600);    // initialize serial communication
  while (!Serial);

  pinMode(LED_BUILTIN, OUTPUT); // initialize the built-in LED pin to indicate when a central is connected

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  /* Set a local name for the BLE device
     This name will appear in advertising packets
     and can be used by remote devices to identify this BLE device
     The name can be changed but maybe be truncated based on space left in advertisement packet
  */
  BLE.setLocalName("BatteryMonitor");
  BLE.setAdvertisedService(batteryService); // add the service UUID
  batteryService.addCharacteristic(batteryLevelChar); // add the battery level characteristic
  BLE.addService(batteryService); // Add the battery service
  //  batteryLevelChar.writeValue(oldBatteryLevel); // set initial value for this characteristic

  /* Start advertising BLE.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */

  // start advertising
  BLE.advertise();

  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // wait for a BLE central
  BLEDevice central = BLE.central();

  if (central && central.connected()) {

    float time_i = micros();
    //    Serial.print(time_i);
    //    Serial.println();

    float ALL_IMU[] = {
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i, time_i,
      time_i
    };

    int packet_size = 54;
    int total_size = (packet_size + 1) * 4;
    byte byteArray[total_size];// 10+1


    for (int i = 0; i < packet_size; i++) {
      byteArray[i * 4] = ((uint8_t*)&ALL_IMU[i])[0];
      byteArray[i * 4 + 1] = ((uint8_t*)&ALL_IMU[i])[1];
      byteArray[i * 4 + 2] = ((uint8_t*)&ALL_IMU[i])[2];
      byteArray[i * 4 + 3] = ((uint8_t*)&ALL_IMU[i])[3];
    }

    byteArray[packet_size * 4] = ((uint8_t*)&time_i)[0];
    byteArray[packet_size * 4 + 1] = ((uint8_t*)&time_i)[1];
    byteArray[packet_size * 4 + 2] = ((uint8_t*)&time_i)[2];
    byteArray[packet_size * 4 + 3] = ((uint8_t*)&time_i)[3];


    //    Serial.print("size of package: ");
    //    Serial.print(sizeof(byteArray));
    //    Serial.println();

    batteryLevelChar.writeValue(byteArray, true);
    count += 1;
    Serial.println(count);
  }

  if (central && !central.connected()) {
    Serial.println("unconnected");
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
    count = 0;
  }

  // if a central is connected to the peripheral:
  //  if (central) {
  //    Serial.print("Connected to central: ");
  //    // print the central's BT address:
  //    Serial.println(central.address());
  //    // turn on the LED to indicate the connection:
  //    digitalWrite(LED_BUILTIN, HIGH);
  //
  //    // check the battery level every 200ms
  //    // while the central is connected:
  //    if (central.connected()) {
  //      long currentMillis = millis();
  //      // if 200ms have passed, check the battery level:
  //      if (currentMillis - previousMillis >= 200) {
  //        previousMillis = currentMillis;
  //        updateBatteryLevel();
  //      }
  //      batteryLevelChar.writeValue(0);
  //      count += 1;
  //    }
  // when the central disconnects, turn off the LED:
  //    digitalWrite(LED_BUILTIN, LOW);
  //    Serial.print("Disconnected from central: ");
  //    Serial.println(central.address());
  //  }


}

//void updateBatteryLevel() {
//  /* Read the current voltage level on the A0 analog input pin.
//     This is used here to simulate the charge level of a battery.
//  */
//  int battery = analogRead(A0);
//  int batteryLevel = map(battery, 0, 1023, 0, 100);
//
//  if (batteryLevel != oldBatteryLevel) {      // if the battery level has changed
//    Serial.print("Battery Level % is now: "); // print it
//    Serial.println(batteryLevel);
//    batteryLevelChar.writeValue(0);  // and update the battery level characteristic
//    oldBatteryLevel = batteryLevel;           // save the level for next comparison
//  }
//}
