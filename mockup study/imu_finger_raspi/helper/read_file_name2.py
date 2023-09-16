import os

def strip_lines(list_lines):
    tmp_list_lines = []
    for line in list_lines:
        tmp_line = line.strip()
        tmp_list_lines.append(tmp_line)
    return tmp_list_lines

def get_user_file_index(user_file_index):
    int_list_user_file_index = []
    for file_index in user_file_index:
        int_list_user_file_index.append(int(file_index))
    return int_list_user_file_index

def get_file_name(list_file_name):
    int_list_file_name = []
    for file_name in list_file_name:
        tmp_file_name_int = [int(x) for x in file_name.split(",")]
        tmp_file_name_int = [x for x in file_name.split(",")]
        # print(tmp_file_name_int)
        int_list_file_name.append(tmp_file_name_int[0])
    return int_list_file_name

def update_user_file_index(list_user_file_index,parent_path,file_index_name):

    user_index = list_user_file_index[0]
    file_index = list_user_file_index[1]
    section_index = list_user_file_index[2]

    file_user_file_index = open(parent_path+"/file_name_tracking/"+file_index_name, "w")
    file_list_name = open(parent_path+"/file_name_tracking/1_selected_videos.txt", "r")
    size_of_file_list = len(file_list_name.readlines())


    if file_index == size_of_file_list - 1:
        user_index = user_index + 1
        file_index = -1

    file_user_file_index.write(str(user_index)+"\n")
    file_user_file_index.write(str(file_index+1)+"\n")
    file_user_file_index.write(str(section_index ))
    file_user_file_index.close()

def create_folder(file_parent_path):
    if not os.path.exists(file_parent_path):
        os.makedirs(file_parent_path)

def get_list_of_file_name(parent_path,IMU_name,ADDunsync=False):  # confirms that the code is under main function

    experiment_result_parent_path = parent_path + "/experiment result/"
    file_index_name = "file_index_"+IMU_name+".txt"
    user_file_index = open(parent_path+"/file_name_tracking/"+file_index_name, "r")
    file_user_name = open(parent_path+"/file_name_tracking/user_name.txt", "r")
    file_file_name = open(parent_path+"/file_name_tracking/1_selected_videos.txt", "r")


    list_user_file_index = get_user_file_index(strip_lines(user_file_index.readlines()))
    list_user_name = strip_lines(file_user_name.readlines())
    list_file_name = get_file_name(strip_lines(file_file_name.readlines()))

    # print(list_user_file_index)
    # print(list_user_name)
    # print(list_file_name)

    # print("user_name:",list_user_name[list_user_file_index[0]])
    # print("sentence#:",list_file_name[list_user_file_index[1]])
    # print("secion#:",list_user_file_index[2])

    user_name = list_user_name[list_user_file_index[0]]
    sentence_num = list_file_name[list_user_file_index[1]]
    section_num = list_user_file_index[2]

    user_file_index.close()
    file_user_name.close()
    file_file_name.close()

    check_add_unsync = lambda x: "_unsync" if (x == True) else ""
    file_parent_path = experiment_result_parent_path + user_name + "/" + \
                       IMU_name+\
                       check_add_unsync(ADDunsync) \
                       + "/"

    if IMU_name not in ["video","imu_info"]:
        file_path = file_parent_path + \
                    user_name + "_" + \
                    str(sentence_num) + \
                    "_section" + str(section_num) + "_" + IMU_name + "_unsync.txt"
    elif IMU_name == "video":
        file_path = file_parent_path + \
                    user_name + "_" + \
                    str(sentence_num) + \
                    "_section" + ".mp4"
    elif IMU_name == "imu_info":
        file_path = file_parent_path + \
                    user_name + "_" + \
                    str(sentence_num) + \
                    "_section" + str(section_num) + "_" + IMU_name + ".txt"


    if ADDunsync == False:
        update_user_file_index(list_user_file_index,parent_path,file_index_name)
    create_folder(file_parent_path)

    # tmp_file = open(file_path, 'w', newline='')
    # tmp_file.close()
    return file_path

def create_file_name_cali(list_user_file_index,list_user_name,parent_path):
    parent_path = parent_path + "/experiment result/cali/"

    section_path = parent_path + "section" + str(list_user_file_index[2]) + "/synced/"
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    section_raw_path = parent_path + "section" + str(list_user_file_index[2]) + "/raw/"
    if not os.path.exists(section_raw_path):
        os.makedirs(section_raw_path)

    tmp_user_cali_path = section_path +list_user_name[list_user_file_index[0]]+"_Section"+ str(list_user_file_index[2]) + "_cali"
    left_hand_imu = tmp_user_cali_path + "_left_tmp.txt"
    right_hand_imu = tmp_user_cali_path + "_right_tmp.txt"

    raw_user_cali_path = section_raw_path + list_user_name[list_user_file_index[0]] + "_Section" + str(
        list_user_file_index[2]) + "_cali"
    left_hand_imu_unsync = raw_user_cali_path + "_left_unsync.txt"
    right_hand_imu_unsync = raw_user_cali_path + "_right_unsync.txt"
    imu_info = raw_user_cali_path + "_imu_info.txt"


    print(left_hand_imu)
    print(right_hand_imu)
    print("")
    print(left_hand_imu_unsync)
    print(right_hand_imu_unsync)
    print(imu_info)

    list_of_file_name = [left_hand_imu,right_hand_imu]
    list_of_file_name_imu = [left_hand_imu_unsync,right_hand_imu_unsync,imu_info]
    return list_of_file_name,list_of_file_name_imu

def get_list_of_file_name_cali(parent_path):
    user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "r")
    file_user_name = open(parent_path+"/file_name_tracking/user_name.txt", "r")

    list_user_file_index = get_user_file_index(strip_lines(user_file_index.readlines()))
    list_user_name = strip_lines(file_user_name.readlines())
    print(list_user_file_index)
    return create_file_name_cali(list_user_file_index, list_user_name,parent_path)


if __name__ == "__main__":
    parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
    print(get_list_of_file_name(parent_path,"right#1"))
    print(get_list_of_file_name(parent_path, "left#1"))
    print(get_list_of_file_name(parent_path, "ear#1"))
    print(get_list_of_file_name(parent_path, "imu_info"))
    print(get_list_of_file_name(parent_path, "video"))
    # get_list_of_file_name_cali()