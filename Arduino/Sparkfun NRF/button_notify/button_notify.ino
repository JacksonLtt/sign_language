// Import libraries (BLEPeripheral depends on SPI)
#include <SPI.h>
#include <BLEPeripheral.h>

//////////////
// Hardware //
//////////////
#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


///////////////////////
// BLE Advertisments //
///////////////////////
const char * localName = "nRF52832 Testing";
BLEPeripheral blePeriph;
BLEService bleServ(SERVICE_UUID);
BLECharCharacteristic btnChar(CHARACTERISTIC_UUID_TX, BLENotify);

void setup()
{
  Serial.begin(115200); // Set up serial at 115200 baud




  setupBLE();
}

void loop()
{
  blePeriph.poll();

  // read the current button pin state
  //  char buttonValue = digitalRead(BTN_PIN);
  //
  //  // has the value changed since the last read
  //  bool buttonChanged = (btnChar.value() != buttonValue);


  // button state changed, update characteristics

  int randnum = random(500);
  Serial.print("random #:");
  Serial.println(randnum);

  btnChar.setValue(randnum);
  delay(1);
}

void setupBLE()
{
  // Advertise name and service:
  blePeriph.setDeviceName(localName);
  blePeriph.setLocalName(localName);
  Serial.println(localName);
  Serial.println(bleServ.uuid());

  blePeriph.setAdvertisedServiceUuid(bleServ.uuid());
  Serial.println(bleServ.uuid());
  // Add service
  blePeriph.addAttribute(bleServ);
//  Serial.println(btnChar);
  // Add characteristic
  blePeriph.addAttribute(btnChar);

  // Now that device, service, characteristic are set up,
  // initialize BLE:
  blePeriph.begin();
}
