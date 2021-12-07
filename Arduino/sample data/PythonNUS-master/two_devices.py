import asyncio
import struct
from bleak import BleakClient

temperatureUUID = "45366e80-cf3a-11e1-9ab4-0002a5d5c51b"
ecgUUID = "46366e80-cf3a-11e1-9ab4-0002a5d5c51b"

notify_uuid = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(0xFFE1)

UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

def callback(sender, data):
    print(sender, data)
    # b = bytearra?y("test", encoding="utf-8")
    f_data = int.from_bytes(data, "big")
    print(f_data)


async def connect_to_device(address):
    print("starting", address, "loop")
    async with BleakClient(address, timeout=5.0) as client:

        print("connect to", address)
        try:
            await client.start_notify(UART_RX_UUID, callback)
            await asyncio.sleep(10.0)
            await client.stop_notify(UART_RX_UUID)
        except Exception as e:
            print(e)

    print("disconnect from", address)


def main(addresses):
    return asyncio.gather(*(connect_to_device(address) for address in addresses))

"""
    mac address
        left hand: A4:E5:7C:C0:04:E2 red board sparkfun esp32
        right hand: D8:A0:1D:5D:7E:FE black board pico
"""

if __name__ == "__main__":
    # asyncio.run(
    #     main(
    #         [
    #             # "A4:E5:7C:C0:04:E2",
    #             # "D8:A0:1D:5D:7E:FE",
    #             "B9EA5233-37EF-4DD6-87A8-2A875E821C46",
    #             "F0CBEBD3-299B-4139-A9FC-44618C720157"
    #         ]
    #     )
    # )
    right_hand = "D8:A0:1D:5D:7E:FE"
    left_hand = "A4:E5:7C:C0:04:E2"
    asyncio.run(asyncio.gather(connect_to_device(right_hand)))
    asyncio.run(asyncio.gather(connect_to_device(left_hand)))