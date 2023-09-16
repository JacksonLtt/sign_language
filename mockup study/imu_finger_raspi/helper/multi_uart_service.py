import asyncio


import sys
import warnings
import struct
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import time
warnings.filterwarnings("ignore", category=DeprecationWarning)

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

count_1 = 0
command = "0"
start_time = time.perf_counter()
stop_time = time.perf_counter()




def unpack_f_bytearray(bytearray):
    f_data = struct.unpack('f', bytearray)
    return f_data[0]

def decode_byte_data(bytedata):
    float_array = []
    for i in range(int(len(bytedata)/4)):

        tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
        float_array.append(tmp_float)
    return float_array

def handle_disconnect(_: BleakClient):
    print(_.address,":Device was disconnected, goodbye.")
    # cancelling all tasks effectively ends the program
    for task in asyncio.all_tasks():
        task.cancel()

def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
    global count_1
    global start_time
    global command
    count_1 += 1

    if count_1 == 1:
        start_time = time.perf_counter()
    # result = decode_byte_data(data)
    # print("count:", count, ",", len(result))
    if command == b's\n':
        result = decode_byte_data(data)
        print("count:",count_1,",",len(result))
        count_1 +=1
        if count_1 == 1:
            start_time = time.perf_counter()
            # print("count = 1 start_time:",start_time)
        # f.write(str(result)[1:-1] + "\n")


async def connect_to_device(address):
    global count_1
    global stop_time
    global start_time
    print("starting", address, "loop")
    async with BleakClient(address, timeout=5.0,disconnected_callback=handle_disconnect) as client:
        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
        print("connect to", address)
        try:
            # await client.start_notify(notify_uuid, callback)
            loop = asyncio.get_running_loop()
            nus = client.services.get_service(UART_SERVICE_UUID)
            rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

            while True:

                data = await loop.run_in_executor(None, sys.stdin.buffer.readline)
                print(address,"data_sent:",data)
                if not data:
                    break

                if data == b's\n':
                    print("START request sent!")
                    count_1 = 0

                if data == b'e\n':
                    print("STOP request sent!")
                    stop_time = time.perf_counter()
                    time_diff = stop_time - start_time
                    print("start_tiem:", start_time, " stop_time:", stop_time, " count:", count_1, " fs:",
                          count_1 / time_diff, " diff:", time_diff)
                    count_1 = 0
                    print("\n")
                    # time.sleep(1)
                    # f.close()

                if data == b'q\n':
                    print("BLE CONN END")
                    break
                # time.sleep(1)
                await client.write_gatt_char(rx_char, data)

        except Exception as e:
            print(e)

    print("disconnect from", address)


def _helper_get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def main(addresses):
    loop = _helper_get_or_create_eventloop()

    # tasks = asyncio.gather(
    #     *(connect_to_device(address) for address in addresses)
    #     # * (self.connect_to_device_keyboard(address, loop, file) for address in addresses)
    #     # * (self.connect_to_device_sshkeyboard(address, loop, file) for address in addresses)
    # )
    ble1 = ('left#1', '737F739D-57CA-4738-B84A-1F34C59783E5')
    ble2 = ('left#2', 'F45E7C56-20A1-487C-AA49-9137616CFF97')

    tasks = asyncio.gather(
        connect_to_device(ble2[1]),
        # * (self.connect_to_device_keyboard(address, loop, file) for address in addresses)
        # * (self.connect_to_device_sshkeyboard(address, loop, file) for address in addresses)
    )
    loop.run_until_complete(tasks)
    # return asyncio.gather(*(connect_to_device(address) for address in addresses))


if __name__ == "__main__":
    try:
        main(
            [
                "737F739D-57CA-4738-B84A-1F34C59783E5",
                # "F45E7C56-20A1-487C-AA49-9137616CFF97",
            ]
        )
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass