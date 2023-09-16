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

def generate_file_name(list_of_folder_name,list_user_file_index,list_user_name, list_file_name):
    user_index = list_user_file_index[0]
    file_index = list_user_file_index[1]
    section_num = list_user_file_index[2]
    # print(user_index)
    # print(file_index)
    # print(section_num)
    # print(list_user_name)
    # print(list_file_name)
    tmp_file_name = list_user_name[user_index] + "_" + str(list_file_name[file_index])


    left_hand_imu_unsync = list_of_folder_name[2]  +tmp_file_name + "_section"+ str(section_num)+ "_left_unsync.txt"
    right_hand_imu_unsync = list_of_folder_name[4] + tmp_file_name + "_section"+ str(section_num)+ "_right_unsync.txt"

    ear_imu = list_of_folder_name[0] + tmp_file_name + "_section" + str(section_num) + "_ear.txt"
    left_hand_imu = list_of_folder_name[1] + tmp_file_name + "_section" + str(section_num) + "_left.txt"
    right_hand_imu = list_of_folder_name[3] + tmp_file_name + "_section" + str(section_num) + "_right.txt"

    video_imu = list_of_folder_name[5] + tmp_file_name + "_section" + str(section_num) + ".mp4"

    imu_info = list_of_folder_name[6] + tmp_file_name + "_section" + str(section_num) + "_imu_info.txt"
    return [ear_imu,left_hand_imu,left_hand_imu_unsync,right_hand_imu,right_hand_imu_unsync,video_imu,imu_info]

def update_user_file_index(list_user_file_index,parent_path):

    user_index = list_user_file_index[0]
    file_index = list_user_file_index[1]
    section_index = list_user_file_index[2]

    file_user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "w")
    file_list_name = open(parent_path+"/file_name_tracking/1_selected_videos.txt", "r")
    size_of_file_list = len(file_list_name.readlines())


    if file_index == size_of_file_list - 1:
        user_index = user_index + 1
        file_index = -1

    file_user_file_index.write(str(user_index)+"\n")
    file_user_file_index.write(str(file_index+1)+"\n")
    file_user_file_index.write(str(section_index ))
    file_user_file_index.close()

def create_folder(list_user_file_index,list_user_name,parent_path):

    user_result_path = parent_path+list_user_name[list_user_file_index[0]]+"/"

    user_result_path_ear = user_result_path + "ear/"
    user_result_path_left = user_result_path + "left/"
    user_result_path_left_unsync = user_result_path + "left_unsync/"
    user_result_path_right = user_result_path + "right/"
    user_result_path_right_unsync = user_result_path + "right_unsync/"
    user_result_path_videos = user_result_path + "videos/"
    user_result_path_info = user_result_path + "info/"

    list_of_folder_name = [user_result_path_ear,user_result_path_left,user_result_path_left_unsync,
                         user_result_path_right,user_result_path_right_unsync,user_result_path_videos,
                           user_result_path_info]

    for folde_name in list_of_folder_name:
        if not os.path.exists(folde_name):
            os.makedirs(folde_name)

    return list_of_folder_name

def get_list_of_file_name(parent_path):  # confirms that the code is under main function

    experiment_result_parent_path = parent_path + "/experiment result/"

    user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "r")
    file_user_name = open(parent_path+"/file_name_tracking/user_name.txt", "r")
    file_file_name = open(parent_path+"/file_name_tracking/1_selected_videos.txt", "r")


    list_user_file_index = get_user_file_index(strip_lines(user_file_index.readlines()))
    list_user_name = strip_lines(file_user_name.readlines())
    list_file_name = get_file_name(strip_lines(file_file_name.readlines()))

    print(list_user_file_index)
    print(list_user_name)
    print(list_file_name)

    # print("user_name:",list_user_name[list_user_file_index[0]])
    # print("sentence#:",list_file_name[list_user_file_index[1]])
    # print("secion#:",list_user_file_index[2])
    user_file_index.close()
    file_user_name.close()
    file_file_name.close()

    update_user_file_index(list_user_file_index,parent_path)

    list_of_folder_name = create_folder(list_user_file_index,list_user_name,experiment_result_parent_path)
    list_of_file_name = generate_file_name(list_of_folder_name,list_user_file_index, list_user_name, list_file_name)

    # for file_name in list_of_folder_name:
    #     print(file_name)
    #
    # print(" ")

    for file_name in list_of_file_name:
        print(file_name)


    return list_of_file_name

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
    print(get_list_of_file_name_cali(parent_path))
    # get_list_of_file_name_cali()