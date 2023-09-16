# echo-client.py

import socket
import time
import asyncio
import sys
import threading
import warnings
from bleak import BleakClient
import keyboard
import sshkeyboard
import struct
from functools import partial



warnings.filterwarnings("ignore", category=DeprecationWarning)


class TCPClient:
    def __init__(self):
        self.Host = "Taitings-MacBook-Pro.local"
        self.Host = "10.0.0.94"
        self.Port = 65432
        self.TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCPClientSocket.connect((self.Host, self.Port))
        self.client_name = socket.gethostname()
        print("client_name:", self.client_name)
        self.IMU_info = self._helper_assign_imu()
        print("IMU_INFO:",self.IMU_info)
        self.count = 0

        self.stop_detected = False
        self.UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # Nordic NUS characteristic for RX
        BLEDevice_addr = [ self.IMU_info["name"],  self.IMU_info['address']]

        self.tmp_add = [BLEDevice_addr]
        self.start_time = time.perf_counter()
        self.end_time = time.perf_counter()

        self.ble_command_rece = False
        t1 = threading.Thread(target=self.recv_msg)
        t1.start()

        # t2 = threading.Thread(target=self.send_msg_sequential)
        # t2.start()
        # self.send_msg_sequential()



    def run_peripheral(self, imu, latency):

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


        mess = str(imu)
        print(mess + "\n")
        mess = mess.encode('utf-8')
        self.TCPClientSocket.send(mess)
        return imu

    def run_connect(self, addresses, file, latency):

        loop = self._helper_get_or_create_eventloop()

        tasks = asyncio.gather(
            # *(self.connect_to_device_latency(address, loop, file, latency) for address in addresses)
            # * (self.connect_to_device_keyboard(address, loop, file) for address in addresses)
            # * (self.connect_to_device_sshkeyboard(address, loop, file) for address in addresses)
            * (self.connect_to_device_socketkeyboard(address, loop, file) for address in addresses)
        )

        loop.run_until_complete(tasks)

    def callback(self, client: BleakClient, file, sender, data):

        self.count += 1
        if self.count == 1:
            # self.start_time = time.perf_counter()
            pass
        else:
            self.end_time = time.perf_counter()

        result = self._helper_decode_byte_data(data)
        # print(len(result),":",result)
        file.write(str(result)[1:-1] + "\n")

    def disconnect_callback(self, client):
        print("Client with address {} got disconnected!".format(client.address))

    def _helper_unpack_f_bytearray(self, bytearray):
        f_data = struct.unpack('f', bytearray)
        return f_data[0]

    def _helper_decode_byte_data(self, bytedata):
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

    async def connect_to_device_latency(self, address, loop, file, latency):
        async with BleakClient(address, loop=loop) as client:


            mess = "connect to "+str(self.IMU_info['name'])
            print(mess)
            mess = mess.encode('utf-8')
            self.TCPClientSocket.send(mess)
            self.start_time = time.time()
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))
                await asyncio.sleep(latency)  # second
                # while True:
                #     if keyboard.is_pressed("q"):
                #         print("STOP connect to ", find_address_name(address))
                #         break
                await client.stop_notify(self.UART_RX_UUID)
                # print("end")
                self.end_time = time.time()

            except KeyboardInterrupt as e:
                print(e)

    async def connect_to_device_keyboard(self, address, loop, file):
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

    async def connect_to_device_sshkeyboard(self, address, loop, file):
        async with BleakClient(address, loop=loop, adapter="hci0") as client:

            print("connect to ", self.IMU_info['name'])
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))

                while True:
                    await sshkeyboard.listen_keyboard_manual(on_press=self._helper_sshkeyboard_press, until="z")
                    print("STOP connect to ", self.IMU_info['name'])
                    break
                await client.stop_notify(self.UART_RX_UUID)

            except Exception as e:
                print(e)

    async def connect_to_device_socketkeyboard(self, address, loop, file):
        async with BleakClient(address, loop=loop, adapter="hci0") as client:

            mess = "connect to " + str(self.IMU_info['name'])
            print(mess)
            mess = mess.encode('utf-8')
            self.TCPClientSocket.send(mess)
            self.start_time = time.time()
            try:
                await client.start_notify(self.UART_RX_UUID, partial(self.callback, client, file))

                while True:
                    if self.stop_detected == True:
                        break
                await client.stop_notify(self.UART_RX_UUID)
                self.end_time = time.time()
            except Exception as e:
                print(e)

    def _helper_sshkeyboard_press(self, key):
        pass
        # print(f"'{key}' pressed")
        # if key == "z":
        #     global detect_z
        #     detect_z = 1

    def recv_msg(self):
        while True:
            recv_msg = self.TCPClientSocket.recv(1024)
            if not recv_msg:
                sys.exit(0)
            recv_msg = recv_msg.decode()
            if recv_msg == "connect_ble":
                print("\n\n")
            print(str(time.time()),":",recv_msg)
            self.decode_message(recv_msg)

    def decode_message(self,message):
        if message == "connect_ble":
            # imu = {"name": "right", "address": "C8:B3:A4:26:46:8F", "path": "right.txt"}
            t_imu = threading.Thread(target=self.run_peripheral,args=(self.IMU_info,10))
            t_imu.start()
            self.stop_detected = False
        elif message == "stop_ble":
            self.stop_detected = True
            # tmp_peripheral.run_peripheral(imu, 10)

    def send_msg(self):
        while True:
            send_msg = input(str("Enter message: "))
            send_msg = send_msg.encode()
            self.TCPClientSocket.send(send_msg)
            print("Message sent")

    def send_msg_sequential(self):
        while True:
            self.TCPClientSocket.send(b"hello from Client")
            print("message sent")
            time.sleep(5)

    def _helper_assign_imu(self):
        if self.client_name == "raspberrypi1":
            return {"name": "left", "address": "DE:1E:16:81:F8:B5",
                    "path": "left.txt"}
        elif self.client_name == "raspberrypi2":
            return {"name": "right", "address": "C8:B3:A4:26:46:8F",
                    "path": "right.txt"}
        elif self.client_name == "raspberrypi3":
            return {"name": "ear", "address": "50:02:91:A1:A3:22",
                    "path": "ear.txt"}
        elif self.client_name == "raspberrypi4":
            return {"name": "right", "address": "C8:B3:A4:26:46:8F",
                    "path": "right.txt"}
        elif self.client_name == "raspberrypi5":
            return {"name": "left", "address": "DE:1E:16:81:F8:B5",
                    "path": "left.txt"}

        return -1

if __name__ == "__main__":
    TCPClient1 = TCPClient()