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
import visualize_imu_data

warnings.filterwarnings("ignore", category=DeprecationWarning)

class BLEDevice():
    def __init__(self,IMU_info):
        self.count = 0
        self.detect_z = 0

        self.UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # Nordic NUS characteristic for RX
        BLEDevice_addr = [IMU_info["name"], IMU_info['address']]

        self.IMU_info = IMU_info
        self.tmp_add = [BLEDevice_addr]
        self.start_time = time.perf_counter()
        self.end_time = time.perf_counter()

    def run_peripheral(self,imu, latency):

        f = open(imu["path"], 'w', newline='')
        while True:
            try:
                self.run_connect([self.IMU_info["address"]], f, latency)
                break
            except Exception as e:
                print(e)
        f.close()

        diff_time = self.end_time - self.start_time
        imu["duration"] = diff_time
        imu["total"] = self.count
        imu["fs"] = float(self.count / diff_time)
        imu["stime"] = self.start_time
        imu["etime"] = self.end_time
        self.count = 0

        print(imu)
        return imu

    def run_connect(self,addresses, file, latency):

        loop = self._helper_get_or_create_eventloop()

        tasks = asyncio.gather(
            *(self.connect_to_device_latency(address, loop, file, latency) for address in addresses)
            # * (self.connect_to_device_keyboard(address, loop, file) for address in addresses)
            # * (self.connect_to_device_sshkeyboard(address, loop, file) for address in addresses)
        )

        loop.run_until_complete(tasks)

    def callback(self,client: BleakClient, file, sender, data):

        self.count += 1
        if self.count == 1:
            self.start_time = time.perf_counter()
        else:
            self.end_time = time.perf_counter()

        result = self._helper_decode_byte_data(data)
        # print(len(result),":",result)
        file.write(str(result)[1:-1] + "\n")

    def disconnect_callback(self,client):
        print("Client with address {} got disconnected!".format(client.address))

    def _helper_unpack_f_bytearray(self,bytearray):
        f_data = struct.unpack('f', bytearray)
        return f_data[0]

    def _helper_decode_byte_data(self,bytedata):
        float_array = []
        for i in range(int(len(bytedata) / 4)):
            tmp_float = self._helper_unpack_f_bytearray(bytedata[i * 4:i * 4 + 4])
            float_array.append(tmp_float)
        return float_array

    def _helper_get_or_create_eventloop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def connect_to_device_latency(self,address, loop, file, latency):
        async with BleakClient(address, loop=loop) as client:

            print("connect to ", self.IMU_info['name'])
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))
                await asyncio.sleep(latency)  # second
                # while True:
                #     if keyboard.is_pressed("q"):
                #         print("STOP connect to ", find_address_name(address))
                #         break
                await client.stop_notify(self.UART_RX_UUID)
                # print("end")


            except KeyboardInterrupt as e:
                print(e)

    async def connect_to_device_keyboard(self,address, loop, file):
        async with BleakClient(address, loop=loop) as client:

            print("connect to ", self.IMU_info['name'])
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))
                # await asyncio.sleep(10)  # second
                while True:
                    await asyncio.sleep(.1)
                    if keyboard.is_pressed("q"):
                        print("STOP connect to ", self.IMU_info['name'])
                        break

                await client.stop_notify(self.UART_RX_UUID)
                # print("end")


            except Exception as e:
                print(e)

    async def connect_to_device_sshkeyboard(self,address, loop, file):
        async with BleakClient(address, loop=loop, adapter="hci0") as client:

            print("connect to ", self.IMU_info['name'])
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))

                while True:
                    await sshkeyboard.listen_keyboard_manual(on_press=self._helper_sshkeyboard_press, until="z")
                    print("STOP connect to ", self.IMU_info['name'])
                    break
                await client.stop_notify(self.UART_RX_UUID)
                print("end")
            except Exception as e:
                print(imu)

    def _helper_sshkeyboard_press(self,key):
        pass
        # print(f"'{key}' pressed")
        # if key == "z":
        #     global detect_z
        #     detect_z = 1

if __name__ == "__main__":
    imu = {"name": "right", "address": "F45E7C56-20A1-487C-AA49-9137616CFF97", "path": "right.txt"}
    # imu = {"name": "right", "address": "C8:B3:A4:26:46:8F", "path": "/home/pi/Desktop/ASL/data_process/right.txt"}
    # imu = {"name": "left","address":'DE:1E:16:81:F8:B5',"path":"left.txt"}
    BLEDevice1 = BLEDevice(imu)
    BLEDevice1.run_peripheral(imu,10)
    file = imu['path']
    visualize_imu_data.readtxt(file)
    # visualize_imu_data.visualize1D_1IMU()
    BLEDevice1.run_peripheral(imu, 10)
    file = imu['path']
    visualize_imu_data.readtxt(file)