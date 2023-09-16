from bleak import BleakClient, discover, BleakError
import asyncio
import struct
from functools import partial
import time
from datetime import datetime
import keyboard
import warnings
# from sshkeyboard import listen_keyboard, stop_listening
# from sshkeyboard import listen_keyboard
import sshkeyboard
import readchar
# import visualize_imu_data

warnings.filterwarnings("ignore", category=DeprecationWarning)
count = 0
detect_z = 0

def press(key):
    pass
    # print(f"'{key}' pressed")
    # if key == "z":
    #     global detect_z
    #     detect_z = 1

UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX

# BLE Mac
peri1_mac = ['left', 'DE:1E:16:81:F8:B5']
peri2_mac = ['right', 'C8:B3:A4:26:46:8F']
peri3_mac = ['ear', '24030208-6F3F-4F9A-BCB9-BC7C39F05388']



tmp_add = [peri1_mac,peri2_mac,peri3_mac]


start_time = time.perf_counter()
end_time = time.perf_counter()

def unpack_f_bytearray(bytearray):
    f_data = struct.unpack('f', bytearray)
    return f_data[0]

def unpack_l_bytearray(bytearray):
    l_data = struct.unpack('l', bytearray)
    return l_data[0]

def decode_byte_data(bytedata):
    float_array = []
    for i in range(int(len(bytedata)/4)):

        tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
        float_array.append(tmp_float)
    return float_array

def callback(client: BleakClient, file, sender,data):
    global start_time
    global end_time
    global count
    count += 1
    if count == 1:
        start_time = time.perf_counter()
    else:
        end_time = time.perf_counter()

    result = decode_byte_data(data)
    # print(len(result),":",result)
    file.write(str(result)[1:-1] + "\n")

def disconnect_callback(client):
    print("Client with address {} got disconnected!".format(client.address))

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def run_connect(addresses,file,latency):

    loop = get_or_create_eventloop()

    tasks = asyncio.gather(
        *(connect_to_device_latency(address, loop, file,latency) for address in addresses)
        # * (connect_to_device_keyboard(address, loop, file) for address in addresses)
        # * (connect_to_device_sshkeyboard(address, loop, file) for address in addresses)
        # * (connect_to_device_readchar(address, loop, file) for address in addresses)

    )

    loop.run_until_complete(tasks)

def find_address_name(address):
    for add in tmp_add:
        if address == add[1]:
            return add[0]

async def connect_to_device_latency(address, loop, file,latency):
    async with BleakClient(address, loop=loop) as client:

        print("connect to ", find_address_name(address))
        try:
            await client.start_notify(UART_RX_UUID, partial(callback, client,file))
            await asyncio.sleep(latency)  # second
            # while True:
            #     if keyboard.is_pressed("q"):
            #         print("STOP connect to ", find_address_name(address))
            #         break
            await client.stop_notify(UART_RX_UUID)
            # print("end")


        except KeyboardInterrupt as e:
            print(e)


async def connect_to_device_keyboard(address, loop, file):
    async with BleakClient(address, loop=loop) as client:

        print("connect to ", find_address_name(address))
        try:
            await client.start_notify(UART_RX_UUID, partial(callback, client,file))
            # await asyncio.sleep(10)  # second
            while True:
                await asyncio.sleep(.1)
                if keyboard.is_pressed("q"):
                    print("STOP connect to ", find_address_name(address))
                    break


            await client.stop_notify(UART_RX_UUID)
            # print("end")


        except Exception as e:
            print(e)

async def connect_to_device_sshkeyboard(address, loop, file):
    async with BleakClient(address, loop=loop,adapter="hci0") as client:

        print("connect to ", find_address_name(address))
        try:
            await client.start_notify(UART_RX_UUID, partial(callback, client,file))

            while True:
                await sshkeyboard.listen_keyboard_manual(on_press=press, until="z")
                print("STOP connect to ", find_address_name(address))
                break
            await client.stop_notify(UART_RX_UUID)
            print("end")
        except Exception as e:
            print(e)
            await asyncio.sleep(5)
            client.stop_notify(UART_RX_UUID)
            file.close()

            diff_time = end_time - start_time
            imu["duration"] = diff_time
            imu["total"] = count - 1
            imu["fs"] = float(count / diff_time)
            imu["stime"] = start_time
            imu["etime"] = end_time

            print(imu)



def run_peripheral(imu,latency):
    f = open(imu["path"], 'w', newline='')

    global count
    while True:
        try:
            run_connect([imu["address"]], f, latency)
            break
        except Exception as e:
            print(e)
    f.close()

    diff_time = end_time-start_time
    imu["duration"] = diff_time
    imu["total"] = count - 1
    imu["fs"] = float(count/diff_time)
    imu["stime"] = start_time
    imu["etime"] = end_time
    count = 0

    print(imu)
    return imu

if __name__ == "__main__":
    # imu = {"name": "right", "address": "F45E7C56-20A1-487C-AA49-9137616CFF97", "path": "right.txt"}
    imu = {"name": "right", "address": "C8:B3:A4:26:46:8F", "path": "right.txt"}
    # imu = {"name": "left","address":'DE:1E:16:81:F8:B5',"path":"left.txt"}
    run_peripheral(imu,5)
    file = imu['path']

    # visualize_imu_data.readtxt(file)
    # visualize_imu_data.visualize1D_1IMU()