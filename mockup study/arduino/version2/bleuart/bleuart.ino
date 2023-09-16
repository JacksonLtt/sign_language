/*********************************************************************
  This is an example for our nRF52 based Bluefruit LE modules

  Pick one up today in the adafruit shop!

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  MIT license, check LICENSE for more information
  All text above, and the splash screen below must be included in
  any redistribution
*********************************************************************/
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>

// BLE Service
BLEDfu  bledfu;  // OTA DFU service
BLEDis  bledis;  // device information
BLEUart bleuart; // uart over ble
BLEBas  blebas;  // battery

float send_time = 2342342;
float ALL_IMU[55] = {
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time, send_time,
  send_time
};

int send_request = 0;
int count_num = 0;
uint32_t rxCount = 0;
uint32_t rxStartTime = 0;
uint32_t rxLastTime = 0;

void setup()
{
  Serial.begin(115200);

#if CFG_DEBUG
  // Blocking wait for connection when debug mode is enabled via IDE
  while ( !Serial ) yield();
#endif

  Serial.println("Bluefruit52 BLEUART Example");
  Serial.println("---------------------------\n");

  // Setup the BLE LED to be enabled on CONNECT
  // Note: This is actually the default behavior, but provided
  // here in case you want to control this LED manually via PIN 19
  Bluefruit.autoConnLed(true);

  // Config the peripheral connection with maximum bandwidth
  // more SRAM required by SoftDevice
  // Note: All config***() function must be called before begin()
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX);

  Bluefruit.begin();
  Bluefruit.setTxPower(4);    // Check bluefruit.h for supported values
  //Bluefruit.setName(getMcuUniqueID()); // useful testing with multiple central connections
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);
  Bluefruit.Periph.setConnInterval(6, 12);
  Bluefruit.setName("right");
  // To be consistent OTA DFU should be added first if it exists
//  bledfu.begin();

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();

  // Configure and Start BLE Uart Service
  bleuart.begin();
  bleuart.setRxCallback(bleuart_rx_callback);

  //  // Start BLE Battery Service
  //  blebas.begin();
  //  blebas.write(100);

  // Set up and start advertising
  startAdv();

  Serial.println("Please use Adafruit's Bluefruit LE app to connect in UART mode");
  Serial.println("Once connected, enter character(s) that you wish to send");
}


void bleuart_rx_callback(uint16_t conn_hdl)
{
  (void) conn_hdl;

  rxLastTime = micros();

  // first packet
  if ( rxCount == 0 )
  {
    rxStartTime = micros();
  }

  uint32_t count = bleuart.available();

//  rxCount += count;
  Serial.print(count);
  if (count == 2) {
    uint8_t ch;
    ch = (uint8_t) bleuart.read();
    Serial.write(ch);
    Serial.println();
    if ( ch == (uint8_t)'s') {
      Serial.println("\nstart_send");
      send_request = 1;
      Serial.print("send_request:");
      Serial.println(send_request);
      count_num = 0;

    }
    else if (ch == (uint8_t)'e') {
      Serial.println("\nend_send");
      send_request = 0;
      Serial.print("send_request:");
      Serial.println(send_request);

    }
  }
  //  Serial.println()
  bleuart.flush(); // empty rx fifo

  // Serial.printf("RX %d bytes\n", count);

  //    // Forward from BLEUART to HW Serial
  //  while ( bleuart.available() )
  //  {
  //    uint8_t ch;
  //    ch = (uint8_t) bleuart.read();
  //    //    Serial.println(ch);
  //    Serial.write(ch);
  //
  //    if ( ch == (uint8_t)'s') {
  //      Serial.println("\nstart_send");
  //      send_request = 1;
  //      Serial.print("send_request:");
  //      Serial.println(send_request);
  //      count_num = 0;
  //
  //    }
  //    else if (ch == (uint8_t)'e') {
  //      Serial.println("\nend_send");
  //      send_request = 0;
  //      Serial.print("send_request:");
  //      Serial.println(send_request);
  //
  //    }
  //  }

}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);

  // Secondary Scan Response packet (optional)
  // Since there is no room for 'Name' in Advertising packet
  Bluefruit.ScanResponse.addName();

  /* Start Advertising
     - Enable auto advertising if disconnected
     - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
     - Timeout for fast mode is 30 seconds
     - Start(timeout) with timeout = 0 will advertise forever (until connected)

     For recommended advertising interval
     https://developer.apple.com/library/content/qa/qa1931/_index.html
  */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

void loop()
{

  if (send_request == 1 && Bluefruit.connected()) {
    //    Serial.print("count:");
    Serial.println(count_num);
    count_num += 1;
    send_message();
  }


}

// callback invoked when central connects
void connect_callback(uint16_t conn_handle)
{
  // Get the reference to current connection
  BLEConnection* connection = Bluefruit.Connection(conn_handle);

  // request PHY changed to 2MB
  Serial.println("Request to change PHY");
  connection->requestPHY();

  // request to update data length
  Serial.println("Request to change Data Length");
  connection->requestDataLengthUpdate();

  // request mtu exchange
  Serial.println("Request to change MTU");
  connection->requestMtuExchange(247);

  char central_name[32] = { 0 };
  connection->getPeerName(central_name, sizeof(central_name));

  Serial.print("Connected to ");
  Serial.println(central_name);
}

void send_message(void)
{
  int packet_size = 54;
  int total_size = (packet_size + 1) * 4;
  byte byteArray[total_size];// 10+1


  for (int i = 0; i < 55; i++) {
    byteArray[i * 4] = ((uint8_t*)&ALL_IMU[i])[0];
    byteArray[i * 4 + 1] = ((uint8_t*)&ALL_IMU[i])[1];
    byteArray[i * 4 + 2] = ((uint8_t*)&ALL_IMU[i])[2];
    byteArray[i * 4 + 3] = ((uint8_t*)&ALL_IMU[i])[3];
  }

  //  byteArray[packet_size * 4] = ((uint8_t*)&send_time)[0];
  //  byteArray[packet_size * 4 + 1] = ((uint8_t*)&send_time)[1];
  //  byteArray[packet_size * 4 + 2] = ((uint8_t*)&send_time)[2];
  //  byteArray[packet_size * 4 + 3] = ((uint8_t*)&send_time)[3];



  size_t sent_data_size = bleuart.write(byteArray, sizeof(byteArray));

}

/**
   Callback invoked when a connection is dropped
   @param conn_handle connection where this event happens
   @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
*/
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  Serial.println();
  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}
