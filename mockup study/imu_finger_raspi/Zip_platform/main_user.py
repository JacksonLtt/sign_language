import asyncio


import sys
import warnings
import struct
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import time
import keyboard
import threading
import read_file_name
import shutil
import json
import data_validation
import sync_hand_imu
import cv2

warnings.filterwarnings("ignore", category=DeprecationWarning)

num_of_imu = 2

command1 = b'-1'
command2 = b'-1'
command3 = b'-1'
command4 = b'-1'
command_last = b'-1'

last_command_remembered = False
sendcommand1 = False
sendcommand2 = False
sendcommand3 = False
sendcommand4 = False

save_info = True
video_ready =  False
video_info = {"name": "video", "path": "bob_47.mp4"}
global BLE1
global BLE2
global BLEEar
# file1 = open("left1", 'w', newline='')

class BLEClass:
    def __init__(self,IMU):
        self.name = IMU["name"]
        self.address = IMU["address"]
        self.file_path = IMU["path"]
        self.parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
        self.file = open(self.file_path, 'w', newline='')
        self.UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
        self.UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
        self.UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
        self.count = 0
        self.command = "0"
        self.start_time = time.time()
        self.stop_time = time.time()
        self.sendcommand = 0
        self.IMUDataInfo = {}
        self.save_to_path = False

    def unpack_f_bytearray(self,bytearray):
        f_data = struct.unpack('f', bytearray)
        return f_data[0]

    def decode_byte_data(self,bytedata):
        float_array = []
        for i in range(int(len(bytedata) / 4)):
            tmp_float = self.unpack_f_bytearray(bytedata[i * 4:i * 4 + 4])
            float_array.append(tmp_float)
        return float_array

    def handle_disconnect(self,_: BleakClient):
        print(self.name, ":Device was disconnected, goodbye.")
        # self.file.close()
        # cancelling all tasks effectively ends the program
        # for task in asyncio.all_tasks():
        #     task.cancel()

    def handle_rx(self,_: BleakGATTCharacteristic, data: bytearray):

        if self.command in [b's\n',b'r\n',b't\n',b'c\n']:
            self.count += 1

            if self.count == 1:
                self.start_time = time.time()
                # print("handle_rx",self.start_time)
            result = self.decode_byte_data(data)
            # print("count:", count, ",", len(result))
            self.file.write(str(result)[1:-1] + "\n")

    def update_command1(self):
        global command1
        global command2
        global command3
        global command4
        global sendcommand1
        global sendcommand2
        global sendcommand3
        global sendcommand4
        if self.name == "left#1":
            self.command = command1
            self.sendcommand = sendcommand1
        elif self.name == "right#1":
            self.command = command2
            self.sendcommand = sendcommand2
        elif self.name == "left#3":
            self.command = command3
            self.sendcommand = sendcommand3
        elif self.name == "ear#1":
            self.command = command4
            self.sendcommand = sendcommand4

    def update_command2(self):
        global command1
        global command2
        global command3
        global command4
        global sendcommand1
        global sendcommand2
        global sendcommand3
        global sendcommand4
        if self.name == "left#1":
            command1 = self.command
            sendcommand1 = self.sendcommand
        elif self.name == "right#1":
            command2 = self.command
            sendcommand2 = self.sendcommand
        elif self.name == "left#3":
            command3 = self.command
            sendcommand3 = self.sendcommand
        elif self.name == "ear#1":
            command4 = self.command
            sendcommand4 = self.sendcommand

    # def get_file_

    async def connect_to_device(self):
        print("starting", self.name, "loop")
        async with BleakClient(self.address, timeout=5.0, disconnected_callback=self.handle_disconnect) as client:
            await client.start_notify(self.UART_TX_CHAR_UUID, self.handle_rx)
            print("connect to", self.name)
            try:

                nus = client.services.get_service(self.UART_SERVICE_UUID)
                rx_char = nus.get_characteristic(self.UART_RX_CHAR_UUID)

                while True:
                    await asyncio.sleep(.1)
                    self.update_command1()
                    if self.sendcommand:
                        self.save_to_path = False
                        # print("sendcommand:", self.sendcommand)
                        if self.command in [ b's\n',b'r\n',b't\n',b'c\n']:
                            # tmp_file = open(self.file_path, "wb+")

                            if not self.file.closed:
                                print("START:",self.name)
                            else:
                                print("START:",self.name)
                                self.file = open(self.file_path, 'w', newline='')
                            self.start_time = time.time()

                        if self.command == b'q\n':
                            # print("BLE CONN END")
                            break

                        if self.command in [b's\n', b'e\n',b'r\n',b't\n',b'c\n']:
                            await client.write_gatt_char(rx_char, self.command)

                        if self.command == b'e\n':
                            print("STOP:",self.name)
                            self.stop_time = time.time()

                            diff_time = self.stop_time - self.start_time


                            if not self.file.closed:
                                self.file.close()


                            self.IMUDataInfo["duration"] = diff_time
                            self.IMUDataInfo["total"] = self.count - 1
                            self.IMUDataInfo["fs"] = float(self.count / diff_time)
                            self.IMUDataInfo["stime"] = self.start_time
                            self.IMUDataInfo["etime"] = self.stop_time
                            self.IMUDataInfo["name"] = self.name
                            self.IMUDataInfo["address"] = self.address
                            self.IMUDataInfo["path"] = self.file_path

                            self.count = 0

                            # print(self.IMUDataInfo)

                            self.save_to_path = True

                        self.sendcommand = False

                    self.update_command2()

            except Exception as e:
                print(e)

        print("disconnect from", self.name)

def copy_imu_file(source_path, dest_path):
    shutil.copyfile(source_path, dest_path)
        # print("{} is copied to {}".format(source_path, dest_path))

def _helper_get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def check_keyboard_press2():
    global command1
    global command2
    global command3
    global command4
    global command_last

    global sendcommand1
    global sendcommand2
    global sendcommand3
    global sendcommand4
    keep_track = True

    while True:
        while True:

            key_press = keyboard.read_key()
            command1 = bytes(str(key_press) + "\n", 'utf-8')
            command2 = command1
            command3 = command1
            command4 = command1

            if command1!=b'e\n':
                command_last = command1


            print("you pressed",key_press)
            time.sleep(0.5)
            # print(time.time(), "command1:", command1)
            # print(time.time(), "command2:", command2)

            if key_press == "z":
                keep_track = False
            break

        sendcommand1 = True
        sendcommand2 = True
        sendcommand3 = True
        sendcommand4 = True
        # print(time.time(), "sendcommand1:", sendcommand1)
        # print(time.time(), "sendcommand2:", sendcommand2)
        if keep_track == False:
            break

def save_dict_to_file(file_path,data):
    with open(file_path, 'w') as convert_file:
        convert_file.write(json.dumps(data))
    print(file_path," is saved!")

def valid_data(list_of_imu_path):
    for imu_path in list_of_imu_path:
        data_validation.one_imu_checker(imu_path)

    # data_validation.video_checker(video_path)

def check_ble_status():
    global BLE1
    global BLE2
    global BLEEar
    global command1
    global command_last
    global save_info
    global video_ready
    global video_info

    while True:
        # print("BLE1_save_to_path:",BLE1.save_to_path)
        # print("BLE2_save_to_path:", BLE2.save_to_path)
        # print("BLEEar_save_to_path:", BLEEar.save_to_path)
        # print("video ready:", video_ready)
        # print("Save Info:", save_info)
        if BLE1.save_to_path \
                and BLE2.save_to_path \
                and BLEEar.save_to_path \
                and video_ready:
            if save_info:
                print("command1:",command1)
                print("command_last:",command_last)
                print("---------")
                list_of_imu_path = [BLE1.IMUDataInfo['path'], BLE2.IMUDataInfo['path'], BLEEar.IMUDataInfo['path']]
                valid_data(list_of_imu_path)

                tmp_imu_data_dic = {}
                parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
                list_of_file_path = []
                if command_last == b's\n':
                    list_of_file_path = read_file_name.get_list_of_file_name(parent_path)
                elif command_last == b'r\n':
                    list_of_file_path = read_file_name.get_list_of_file_name(parent_path,1)

                # validate IMU data


                dict_file_path = list_of_file_path[6]
                video_file_path = list_of_file_path[5]

                print("---------")
                copy_imu_file(BLE1.file_path, list_of_file_path[2])
                copy_imu_file(BLE2.file_path, list_of_file_path[4])
                copy_imu_file(BLEEar.file_path, list_of_file_path[0])
                print(video_info['path'],"-----",video_file_path)

                copy_imu_file(video_info['path'],video_file_path)
                BLE1.IMUDataInfo['path'] = list_of_file_path[2]
                BLE2.IMUDataInfo['path'] = list_of_file_path[4]
                BLEEar.IMUDataInfo['path'] = list_of_file_path[0]
                video_info['path'] = video_file_path
                print(BLE1.IMUDataInfo)
                print(BLE2.IMUDataInfo)
                print(BLEEar.IMUDataInfo)
                print(video_info)

                tmp_imu_data_dic[BLE1.name] =BLE1.IMUDataInfo
                tmp_imu_data_dic[BLE2.name] = BLE2.IMUDataInfo
                tmp_imu_data_dic[BLEEar.name] = BLEEar.IMUDataInfo
                tmp_imu_data_dic[video_info["name"]] = video_info
                print("---------")



                #sync left hand and right hand data
                tmp_sync_imu = {}
                tmp_sync_imu[BLE1.name] = BLE1.IMUDataInfo
                tmp_sync_imu[BLE2.name] = BLE2.IMUDataInfo
                syncimu = sync_hand_imu.SYNCIMU(tmp_sync_imu)
                tmp_sync_data = syncimu.load_files()

                syncimu.save_data(list_of_file_path[1], tmp_sync_data[0])
                syncimu.save_data(list_of_file_path[3], tmp_sync_data[1])
                save_dict_to_file(dict_file_path, tmp_imu_data_dic)
                print(video_info['path']," is saved!")
                print("\n")
                video_info['path'] = "bob_42.mp4"
                BLE1.IMUDataInfo['path'] = "left.txt"
                BLE2.IMUDataInfo['path'] = "right.txt"
                BLEEar.IMUDataInfo['path'] = "ear.txt"
                save_info = False
        else:
            save_info = True

        if command1 == b'z\n':
            break
        # time.sleep(5)


def check_ble_status_cali():
    global BLE1
    global BLE2
    global command1
    global command_last
    global save_info

    while True:
        if BLE1.save_to_path and BLE2.save_to_path:
            if save_info:
                print("command1:", command1)
                print("command_last:", command_last)

                print("---------")

                # validate IMU data
                list_of_imu_path = [BLE1.IMUDataInfo['path'], BLE2.IMUDataInfo['path']]
                valid_data(list_of_imu_path)


                tmp_imu_data_dic = {}
                parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
                list_of_file_path = []
                if command_last == b's\n':
                    list_of_file_path = read_file_name.get_list_of_file_name_cali(parent_path)

                for i in list_of_file_path:
                    print(i)

                dict_file_path = list_of_file_path[4]


                print("---------")
                copy_imu_file(BLE1.file_path, list_of_file_path[2])
                copy_imu_file(BLE2.file_path, list_of_file_path[3])

                # sync left hand and right hand data
                tmp_sync_imu = {}
                tmp_sync_imu[BLE1.name] = BLE1.IMUDataInfo
                tmp_sync_imu[BLE2.name] = BLE2.IMUDataInfo
                syncimu = sync_hand_imu.SYNCIMU(tmp_sync_imu)
                tmp_sync_data = syncimu.load_files()

                syncimu.save_data(list_of_file_path[0], tmp_sync_data[0])
                syncimu.save_data(list_of_file_path[1], tmp_sync_data[1])

                BLE1.IMUDataInfo['path'] = list_of_file_path[0]
                BLE2.IMUDataInfo['path'] = list_of_file_path[1]
                print(BLE1.IMUDataInfo)
                print(BLE2.IMUDataInfo)

                tmp_imu_data_dic[BLE1.name] = BLE1.IMUDataInfo
                tmp_imu_data_dic[BLE2.name] = BLE2.IMUDataInfo

                save_dict_to_file(dict_file_path, tmp_imu_data_dic)
                BLE1.IMUDataInfo['path'] = "left.txt"
                BLE2.IMUDataInfo['path'] = "right.txt"

                save_info = False
        else:
            save_info = True

        if command1 == b'z\n':
            break


def check_ble_status_one_hand():
    global BLE1
    # global BLE2
    global command1
    global command_last
    global save_info

    while True:
        if BLE1.save_to_path and BLE2.save_to_path:
            if save_info:
                print("command1:", command1)
                print("command_last:", command_last)

                print("---------")

                # validate IMU data
                list_of_imu_path = [BLE1.IMUDataInfo['path']]
                valid_data(list_of_imu_path)


                tmp_imu_data_dic = {}
                parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
                list_of_file_path = []
                if command_last == b's\n':
                    list_of_file_path = read_file_name.get_list_of_file_name_cali(parent_path)

                for i in list_of_file_path:
                    print(i)

                dict_file_path = list_of_file_path[4]


                print("---------")
                copy_imu_file(BLE1.file_path, list_of_file_path[2])
                # copy_imu_file(BLE2.file_path, list_of_file_path[3])

                # sync left hand and right hand data
                tmp_sync_imu = {}
                tmp_sync_imu[BLE1.name] = BLE1.IMUDataInfo
                # tmp_sync_imu[BLE2.name] = BLE2.IMUDataInfo
                # syncimu = sync_hand_imu.SYNCIMU(tmp_sync_imu)
                # tmp_sync_data = syncimu.load_files()

                # syncimu.save_data(list_of_file_path[0], tmp_sync_imu[0])
                # syncimu.save_data(list_of_file_path[1], tmp_sync_data[1])

                BLE1.IMUDataInfo['path'] = list_of_file_path[0]
                # BLE2.IMUDataInfo['path'] = list_of_file_path[1]
                print(BLE1.IMUDataInfo)
                # print(BLE2.IMUDataInfo)

                tmp_imu_data_dic[BLE1.name] = BLE1.IMUDataInfo
                # tmp_imu_data_dic[BLE2.name] = BLE2.IMUDataInfo

                save_dict_to_file(dict_file_path, tmp_imu_data_dic)
                BLE1.IMUDataInfo['path'] = "left.txt"
                # BLE2.IMUDataInfo['path'] = "right.txt"

                save_info = False
        else:
            save_info = True

        if command1 == b'z\n':
            break

def make_1080p(video):
    video.set(3, 1920)
    video.set(4, 1080)

def captrure_video_keyboard(video_info):
    global command1
    global video_ready

    video = cv2.VideoCapture(0)

    if (video.isOpened() == False):
        print("Error reading video file")

    make_1080p(video)

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))


    size = (frame_width, frame_height)
    result = cv2.VideoWriter(video_info["path"],cv2.VideoWriter_fourcc('m', 'ps', '4', 'v'),30, size)
    start_time = time.perf_counter()
    list_of_frame = []

    video_ready = False
    start = False
    try:
        while True:

            if command1  in [ b's\n',b'r\n',b't\n',b'c\n']:
                ret, frame = video.read()
                if start == False:
                    start_time = time.time()
                    print("START: video")
                start = True
                frame2 = cv2.flip(frame, 1)
                list_of_frame.append(frame2)

            if command1 == b'e\n':
                end_time = time.time()
                print("STOP Video")
                break


    except KeyboardInterrupt:
        pass

    print("START saving")
    # print(list_of_frame)
    for fram in list_of_frame:
        result.write(fram)

    video.release()
    result.release()
    cv2.destroyAllWindows()

    # print(result)
    # print("{} video is saved!".format(video_info['path']))
    video_info['duration'] = end_time - start_time
    video_info['stime'] = start_time
    video_info['etime'] = end_time
    # print(video_info)
    video_ready = True
    return video_info

def video_capture_keyboard():
    # global video_ready
    global video_info

    while True:
        if command1 in [ b's\n',b'r\n',b't\n',b'c\n']:
            # video_ready = False
            video_info = captrure_video_keyboard(video_info)
            # video_ready = True
        if command1 == b'z\n':
            break

def main():
    global BLE1
    global BLE2
    global BLEEar

    keyboard_detect_thread = threading.Thread(target=check_keyboard_press2)
    keyboard_detect_thread.start()

    loop = _helper_get_or_create_eventloop()

    IMU1 = {"name":"left#1","address":"2A9F4C95-0B8A-4389-B697-834378A0A51B","path":"left.txt"}
    IMU2 = {"name":"right#1","address":"F45E7C56-20A1-487C-AA49-9137616CFF97","path":"right.txt"}

    # IMU1 = {"name": "left#2", "address": "737F739D-57CA-4738-B84A-1F34C59783E5", "path": "left.txt"}
    # IMU2 = {"name": "right#2", "address": "4A2E4807-BA85-444A-BF19-3752CF6E71B2", "path": "right.txt"}

    # IMU3 = {"name":'left#3', "address":"2A9F4C95-0B8A-4389-B697-834378A0A51B","path":list_of_path[2]}
    IMUEar = {"name":'ear#1',"address":'24030208-6F3F-4F9A-BCB9-BC7C39F05388',"path":"ear.txt"}


    BLE1 = BLEClass(IMU1)
    BLE2 = BLEClass(IMU2)
    # BLEC3 = BLEClass(IMU3)
    BLEEar = BLEClass(IMUEar)

    check_BLE_status_thread = threading.Thread(target=check_ble_status)
    check_BLE_status_thread.start()

    video_capture_thread = threading.Thread(target=video_capture_keyboard)
    video_capture_thread.start()

    tasks = asyncio.gather(
        BLE1.connect_to_device(),
        BLE2.connect_to_device(),
        # BLEC3.connect_to_device(),
        BLEEar.connect_to_device(),
    )
    loop.run_until_complete(tasks)
    # return asyncio.gather(*(connect_to_device(address) for address in addresses))


def cali():
    global BLE1
    global BLE2

    keyboard_detect_thread = threading.Thread(target=check_keyboard_press2)
    keyboard_detect_thread.start()

    loop = _helper_get_or_create_eventloop()

    IMU1 = {"name": "left#1", "address": "2A9F4C95-0B8A-4389-B697-834378A0A51B", "path": "left.txt"}
    IMU2 = {"name": "right#1", "address": "F45E7C56-20A1-487C-AA49-9137616CFF97", "path": "right.txt"}

    # IMU1 = {"name": "left#2", "address": "737F739D-57CA-4738-B84A-1F34C59783E5", "path": "left.txt"}
    # IMU2 = {"name": "right#2", "address": "4A2E4807-BA85-444A-BF19-3752CF6E71B2", "path": "right.txt"}

    BLE1 = BLEClass(IMU1)
    BLE2 = BLEClass(IMU2)


    check_BLE_status_thread = threading.Thread(target=check_ble_status_cali)
    check_BLE_status_thread.start()


    tasks = asyncio.gather(
        BLE1.connect_to_device(),
        BLE2.connect_to_device(),
    )

    loop.run_until_complete(tasks)

def one_hand():
    global BLE1

    keyboard_detect_thread = threading.Thread(target=check_keyboard_press2)
    keyboard_detect_thread.start()

    loop = _helper_get_or_create_eventloop()

    IMU1 = {"name": "left#1", "address": "2A9F4C95-0B8A-4389-B697-834378A0A51B", "path": "left.txt"}
    # IMU2 = {"name": "right#1", "address": "F45E7C56-20A1-487C-AA49-9137616CFF97", "path": "right.txt"}

    # IMU1 = {"name": "left#2", "address": "737F739D-57CA-4738-B84A-1F34C59783E5", "path": "left.txt"}
    # IMU2 = {"name": "right#2", "address": "4A2E4807-BA85-444A-BF19-3752CF6E71B2", "path": "right.txt"}

    BLE1 = BLEClass(IMU1)
    # BLE2 = BLEClass(IMU2)


    check_BLE_status_thread = threading.Thread(target=check_ble_status_one_hand)
    check_BLE_status_thread.start()


    tasks = asyncio.gather(
        BLE1.connect_to_device(),
        # BLE2.connect_to_device(),
    )

    loop.run_until_complete(tasks)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        is_main = int(sys.argv[1])
        if is_main == 1:
            try:
                # print(list_of_path)
                main()
            except asyncio.CancelledError:
                # task is cancelled on disconnect, so we ignore this error
                pass
    elif len(sys.argv) == 2:
        is_main = int(sys.argv[1])
        if is_main == 2:
            try:
                # print(list_of_path)
                one_hand()
            except asyncio.CancelledError:
                # task is cancelled on disconnect, so we ignore this error
                pass
    else:
        cali()
