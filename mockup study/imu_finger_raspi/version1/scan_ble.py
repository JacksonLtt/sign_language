import asyncio
from bleak import BleakScanner

async def scan_device():
    devices = await BleakScanner.discover(adapter="hci0")
    list_devices_name =[(d.name,d.address) for d in devices if d.name != '']
    # print(list_devices_name)
    return list_devices_name




def find_device(list_of_target_ble_name):
    list_name = asyncio.run(scan_device())

    result = True
    list_name = [x[0] for x in list_name]
    for target_ble_name in list_of_target_ble_name:
        if target_ble_name in list_name:
            result = result and True
            print("BLE device \"{}\" is found!".format(target_ble_name))
        else:
            print("BLE device \"{}\" is NOT found!".format(target_ble_name))
            result = result and False


    return result


def show_device():
    list_name = asyncio.run(scan_device())

    for name in list_name:
        # if name[0] != "Unknown" and name[0].replace("-",":") != name[1]:
        #
        #     print(name)
        print(name)
    # print(list_name)


if __name__ == "__main__":
    show_device()

