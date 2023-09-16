import runpy
import multiprocessing
import time
import tmp_peripheral
import sys
import os
import read_file_name
import sync_hand_imu
import shutil
import json
import scan_ble
import os.path
import data_validation
import video_capture

def run_peri(imu,latency,imu_data_dict):
    tmp_imu_data_dict = tmp_peripheral.run_peripheral(imu,latency)
    imu_data_dict[imu['name']]= tmp_imu_data_dict

def run_peri_video(imu,imu_data_dict):
    tmp_imu_data_dict = video_capture.captrure_video_keyboard(imu)
    imu_data_dict[imu['name']]= tmp_imu_data_dict

def copy_imu_file(source_path,dest_path):
    shutil.copyfile(source_path, dest_path)
    print("{} is copied to {}".format(source_path[71:],dest_path[71:]))

def save_dict_to_file(file_path,data):
    with open(file_path, 'w') as convert_file:
        convert_file.write(json.dumps(data))

def check_files_exit(list_of_file):
    for i in range(len(list_of_file)):
        if os.path.exists(list_of_file[i]) == False:
            return False
    print("all raw files exit!")
    return True

def main_get_sentence():
    list_of_target_ble = ['right', 'left', 'ear']
    if scan_ble.find_device(list_of_target_ble):
        imu_dict = {}
        imu_dict["left"] = {}
        imu_dict["left"]["name"] = "left"
        imu_dict["left"]["address"] = '2A9F4C95-0B8A-4389-B697-834378A0A51B'
        imu_dict["right"] = {}
        imu_dict["right"]["name"] = "right"
        imu_dict["right"]["address"] = 'F45E7C56-20A1-487C-AA49-9137616CFF97'
        imu_dict["ear"] = {}
        imu_dict["ear"]["name"] = "ear"
        imu_dict["ear"]["address"] = '24030208-6F3F-4F9A-BCB9-BC7C39F05388'
        imu_dict["video"] = {}
        imu_dict["video"]["name"] = "video"
        parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"

        list_of_file_name = read_file_name.get_list_of_file_name(parent_path)
        imu_dict['left']["path"] = list_of_file_name[2]
        imu_dict['right']["path"] = list_of_file_name[4]
        imu_dict['video']['path'] = list_of_file_name[5]
        imu_dict['ear']['path'] = list_of_file_name[0]

        print("")

        procs = []
        latency = 20

        process_manager = multiprocessing.Manager()
        imu_data_dict = process_manager.dict()

        tmp_proc = multiprocessing.Process(target=run_peri, args=(
            imu_dict["left"], latency, imu_data_dict))  # instantiating without any argument
        procs.append(tmp_proc)
        tmp_proc.start()

        tmp_proc = multiprocessing.Process(target=run_peri, args=(
            imu_dict["right"], latency, imu_data_dict))  # instantiating without any argument
        procs.append(tmp_proc)
        tmp_proc.start()

        tmp_proc = multiprocessing.Process(target=run_peri, args=(
            imu_dict["ear"], latency, imu_data_dict))  # instantiating without any argument
        procs.append(tmp_proc)
        tmp_proc.start()

        tmp_proc = multiprocessing.Process(target=run_peri_video, args=(
            imu_dict["video"], imu_data_dict))
        procs.append(tmp_proc)
        tmp_proc.start()

        # complete the processes
        for proc in procs:
            proc.join()

        save_dict_to_file(list_of_file_name[6], imu_data_dict.copy())

        tmp_list_of_file_name = list_of_file_name.copy()
        tmp_list_of_file_name.remove(tmp_list_of_file_name[1])
        tmp_list_of_file_name.remove(tmp_list_of_file_name[2])
        while check_files_exit(tmp_list_of_file_name) == False:
            pass



        # validation_result = data_validation.hand_imu_fre_checker(list_of_file_name[0],list_of_file_name[1],
        #                                      imu_data_dict['left']['fs'],imu_data_dict['right']['fs'],
        #                                      imu_data_dict['left']['total'],imu_data_dict['right']['total'])

        # validation_result = data_validation.hand_imu_fre_checker(list_of_file_name[0], list_of_file_name[1],
        #                                                          imu_data_dict['left']['fs'],
        #                                                          imu_data_dict['right']['fs'],
        #                                                          imu_data_dict['left']['total'],
        #                                                          imu_data_dict['right']['total']) and \
        #                     data_validation.one_imu_checker(list_of_file_name[3])
                            # data_validation.video_checker(list_of_file_name[2])

        for file_name in list_of_file_name:
            print(file_name)
        if True:
        # if validation_result:
            data = sync_hand_imu.load_files(imu_data_dict)
            sync_hand_imu.save_data(list_of_file_name[1], data[0])
            sync_hand_imu.save_data(list_of_file_name[3], data[1])
        else:
            print("validation failed!")



def main_cali():
    list_of_target_ble = ['left#1', 'right#1']
    if scan_ble.find_device(list_of_target_ble):
        imu_dict = {}
        imu_dict[list_of_target_ble[0]] = {}
        imu_dict[list_of_target_ble[0]]["name"] = list_of_target_ble[0]
        imu_dict[list_of_target_ble[0]]["address"] = '2A9F4C95-0B8A-4389-B697-834378A0A51B'
        imu_dict[list_of_target_ble[1]] = {}
        imu_dict[list_of_target_ble[1]]["name"] = list_of_target_ble[1]
        imu_dict[list_of_target_ble[1]]["address"] = 'F45E7C56-20A1-487C-AA49-9137616CFF97'

        parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
        list_of_file_name, list_of_file_name_imu = read_file_name.get_list_of_file_name_cali(parent_path)

        imu_dict[list_of_target_ble[0]]["path"] = list_of_file_name[0]
        imu_dict[list_of_target_ble[1]]["path"] = list_of_file_name[1]


        print("")

        procs = []
        latency = 5

        process_manager = multiprocessing.Manager()
        imu_data_dict = process_manager.dict()

        tmp_proc = multiprocessing.Process(target=run_peri, args=(
            imu_dict[list_of_target_ble[0]], latency, imu_data_dict))  # instantiating without any argument
        procs.append(tmp_proc)
        tmp_proc.start()

        tmp_proc = multiprocessing.Process(target=run_peri, args=(
            imu_dict[list_of_target_ble[1]], latency, imu_data_dict))  # instantiating without any argument
        procs.append(tmp_proc)
        tmp_proc.start()


        # complete the processes
        for proc in procs:
            proc.join()

        while check_files_exit(list_of_file_name) == False:
            pass

        copy_imu_file(list_of_file_name[0], list_of_file_name_imu[0])
        copy_imu_file(list_of_file_name[1], list_of_file_name_imu[1])

        save_dict_to_file(list_of_file_name_imu[2],imu_data_dict.copy())


        data = sync_hand_imu.load_files(imu_data_dict)
        sync_hand_imu.save_data(imu_data_dict[list_of_target_ble[0]]["path"][:-8] + ".txt", data[0])
        sync_hand_imu.save_data(imu_data_dict[list_of_target_ble[1]]["path"][:-8] + ".txt", data[1])

        os.remove(list_of_file_name[0])
        os.remove(list_of_file_name[1])


if __name__ == "__main__":  # confirms that the code is under main function
    if len(sys.argv) == 2:
        is_cali = int(sys.argv[1])
        if is_cali == 1:
            main_get_sentence()
    else:
        main_cali()
