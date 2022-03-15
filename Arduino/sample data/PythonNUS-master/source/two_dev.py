import asyncio
from bleak import BleakClient
from functools import partial
import struct


count_left = 0
count_right = 0
# CHAR_UUID = "00000080-0001-11e1-ac36-0002a5d5c51b".format(0xFFE1)
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

def callback(client: BleakClient, sender: int, data: bytearray):
    hex_string = data.hex()
    # print(f"{client.address}", "".join([hex_string[x:x + 2] for x in range(0, len(hex_string), 2)]))
    print(client.address, ":", data)
    result = struct.unpack('l', data + bytes([0, 0, 0]))[0]

    global count_left
    global count_right
    if result == 0:
        print(sender, ": left count: ", count_left, "result", result)
        count_left += 1

    if result == 1:
        print(sender, ": right count: ", count_right, "result", result)
        count_right += 1

def run(addresses):
    loop = asyncio.get_event_loop()
    loop1 = asyncio.get_event_loop()

    for address in addresses:
        try:
            loop.create_task(connect_to_device(address))
        except Exception as e:
            loop.stop()
            address = address
            loop1.create_task(connect_to_device(address))


    loop.run_until_complete()
    loop1.run_until_complete()


async def connect_to_device(address):
    async with BleakClient(address, timeout=20.0, use_cached=False) as client:
        print(f"Connected: {address} {client.is_connected}")
        await asyncio.sleep(0.8)
        # while True:
        #     await client.start_notify(UART_RX_UUID, partial(callback, client))
        try:
            # x = await client.is_connected()
            # print("Connected: {0}".format(x))
            # await client.start_notify(UART_RX_UUID, callback)
            await client.start_notify(UART_RX_UUID,  partial(callback, client))
            await asyncio.sleep(1)
            await client.stop_notify(UART_RX_UUID)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run(["A4:E5:7C:C0:04:E2", "D8:A0:1D:5D:7E:FE"])