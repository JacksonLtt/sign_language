"""
UART Service
-------------

An example showing how to write a simple program using the Nordic Semiconductor
(nRF) UART service.

"""

import asyncio
import sys
import time
from itertools import count, takewhile
from typing import Iterator
import os
import struct

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import bleak
UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

count = 0
start_time = time.perf_counter()
stop_time = time.perf_counter()
# os.system('pip3 show bleak')
# ('left#2', 'F45E7C56-20A1-487C-AA49-9137616CFF97')
# ('left#1', '737F739D-57CA-4738-B84A-1F34C59783E5')
# ('left#2', 'F45E7C56-20A1-487C-AA49-9137616CFF97')
# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


def unpack_f_bytearray(bytearray):
    f_data = struct.unpack('f', bytearray)
    return f_data[0]


def decode_byte_data(bytedata):
    float_array = []
    for i in range(int(len(bytedata)/4)):

        tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
        float_array.append(tmp_float)
    return float_array


async def uart_terminal():
    """This is a simple "terminal" program that uses the Nordic Semiconductor
    (nRF) UART service. It reads from stdin and sends each line of data to the
    remote device. Any data received from the device is printed to stdout.
    """

    def match_nus_uuid(device: BLEDevice, adv: AdvertisementData,target_name):
        # This assumes that the device includes the UART service UUID in the
        # advertising data. This test may need to be adjusted depending on the
        # actual advertising data supplied by the device.
        if device.name == target_name:
            return True

        return False

    # device = await BleakScanner.find_device_by_filter(match_nus_uuid)
    ble_addr = 'F45E7C56-20A1-487C-AA49-9137616CFF97'
    device = await BleakScanner.find_device_by_address(ble_addr)
    print("device:",device,type(device))
    if device is None:
        print("no matching device found, you may need to edit match_nus_uuid().")
        sys.exit(1)

    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        global count
        global start_time
        result = decode_byte_data(data)
        # print("count:",count,",",len(result),":",result)
        count +=1
        if count == 1:
            start_time = time.perf_counter()
            # print("count = 1 start_time:",start_time)
        f.write(str(result)[1:-1] + "\n")

    async with BleakClient(device, disconnected_callback=handle_disconnect) as client:
        global count
        global stop_time
        global start_time
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        print("Connected, start typing and press ENTER...")

        loop = asyncio.get_running_loop()
        nus = client.services.get_service(UART_SERVICE_UUID)
        rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

        while True:
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
            if not data:
                break

            if data == b's\n':
                print("START request sent!")
                count = 0

            if data == b'e\n':
                print("STOP request sent!")
                stop_time = time.perf_counter()
                time_diff = stop_time - start_time
                print("start_tiem:",start_time," stop_time:",stop_time," count:",count," fs:",count/time_diff," diff:", time_diff)
                count = 0
                print("\n")
                # time.sleep(1)
                # f.close()

            if data == b'q\n':
                print("BLE CONN END")
                break

            await client.write_gatt_char(rx_char, data)


f = open("right.txt", 'w', newline='')
if __name__ == "__main__":
    try:

        asyncio.run(uart_terminal())
        # pass
    # except Exception as e:
    #     print(e)
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass