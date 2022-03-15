import asyncio
from bleak import BleakScanner

async def scan_device():
    devices = await BleakScanner.discover()
    list_devices_name =[(d.name,d.address) for d in devices if d.name != '']
    return list_devices_name


def find_device(name):
    list_name = asyncio.run(scan_device())
    for name in list_name:

        print(name)
    # print(list_name)
    return name in list_name

print(find_device("BatteryMonitor"))

