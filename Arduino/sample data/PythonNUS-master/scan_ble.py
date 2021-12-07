import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover()
    list_devices =[]
    for d in devices:
        print(d)
        # list_devices.append(d[20:])



asyncio.run(main())
