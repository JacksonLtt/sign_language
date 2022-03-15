"""
Coyt Barringer - 2020

Test program demonstrating data transmission between Adafruit Bluefruit BLE libraries running 
on nrf52840 and Python

This uses the Nordic Uart Service (NUS) and should work concurrently with other BLE services such as HID

On the python side, the Bluetooth Low Energy platform Agnostic Klient for Python (Bleak) project
is used for Cross Platform Support and has been tested with windows 10

"""

import platform
import logging
import asyncio
from bleak import BleakClient
from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict
import sys
import datetime;
import csv
import struct

import _thread
import threading
import time

UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

dataFlag = False #global flag to check for new data
count = 0

def unpack_f_bytearray(bytearray):
    f_data = struct.unpack('f', bytearray)
    return f_data[0]

def unpack_l_bytearray(bytearray):
    l_data = struct.unpack('l', bytearray)
    return l_data[0]

def decode_byte_data(bytedata):
    float_array = []
    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:] + bytes([0, 0, 0, 0]))) # macos struct.error: unpack requires a buffer of 8 bytes
    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:] ))   # macos struct.error: unpack requires a buffer of 4 bytes
    for i in range(int(len(bytedata)/4)-1):

        tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
        float_array.append(tmp_float)

    float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:] + bytes([0, 0, 0, 0])))
    return float_array


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""

    # print("re:",list(data))
    global count

    result = decode_byte_data(data)
    print(threading.current_thread().name," ",len(result),"count: ",count,"result",result)
    count +=1

    # if count == 3000:
    #     while(True):
    #         pass
    f.write("["+str(result)[1:-2]+"]\n")
    # print(str(result)[1:-2])
    global dataFlag
    dataFlag = True


async def run(address, loop):

    async with BleakClient(address, loop=loop) as client:
        try:
            #wait for BLE client to be connected
            x = await client.is_connected()

            print("Connected: {0}".format(x))

            #wait for data to be sent from client
            await client.start_notify(UART_RX_UUID, notification_handler)


            while True :

                #give some time to do other tasks
                await asyncio.sleep(0.01)

                #check if we received data
                global dataFlag
                if dataFlag :
                    dataFlag = False

                    #echo our received data back to the BLE device
                    # data = await client.read_gatt_char(UART_RX_UUID)
                    # await client.write_gatt_char(UART_TX_UUID,data)
        finally:
            print("end")
            await client.disconnect()

# f = open("/Users/taitinglu/Documents/GitHub/Tapstrap/Arduino/BLE/PythonNUS-master/7.txt",'w',newline='') # macos
f = open("C:/Users/txl5518/Documents/Github/sign_language/Arduino/sample data/PythonNUS-master/7.txt",'w',newline='')
# f = open("C:/Users/txl5518/Documents/Github/Tapstrap/Arduino/BLE/PythonNUS-master/11022021_ble.txt",'w',newline='') # windows
# f = open("C:/Users/txl5518/Documents/Github/Tapstrap/Arduino/BLE/PythonNUS-master/11022021_ble.txt",'w',newline='')



"""
    mac address
        left hand: A4:E5:7C:C0:04:E2 red board sparkfun esp32
        right hand: D8:A0:1D:5D:7E:FE black board pico
"""

def receive_data_by_ble(address,loop):
    # this is MAC of our BLE device
    loop.run_until_complete(run(address, loop))

    f.close()


if __name__ == "__main__":
    address_left_hand = (
        # "BA50F048-9E22-4C79-95C0-6EBBD28E5B20" # nodemcu eps32 mac
        # "E08FC2D4-E70E-42B0-A767-07A6F555736C" # tinypico mac
        # "A4:E5:7C:C0:04:E2"
        # "07152EF7-3379-4B6F-BDD3-53F56237EBD8"
        "50:02:91:A1:AA:30" #tinypico windows
    )

    address_right_hand = (
        "D8:A0:1D:5D:7E:FE"
    )
    loop = asyncio.get_event_loop()

    left_hand_thread = threading.Thread(target=receive_data_by_ble,args=(address_left_hand, loop,))
    left_hand_thread.start()
    right_hand_thread = threading.Thread(target=receive_data_by_ble, args=(address_right_hand, loop,))
    right_hand_thread.start()