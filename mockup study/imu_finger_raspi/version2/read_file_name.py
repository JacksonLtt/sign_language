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
        # tmp_file_name_int = [int(x) for x in file_name.split(",")]
        tmp_file_name_int = [x for x in file_name.split(",")]
        # print(tmp_file_name_int)
        int_list_file_name.append(tmp_file_name_int[0])
    return int_list_file_name

def generate_file_name(list_of_folder_name,list_user_file_index,list_user_name, list_file_name,copy_version = 0):
    user_index = list_user_file_index[0]
    file_index = list_user_file_index[1]
    section_num = list_user_file_index[2]
    # print(user_index)
    # print(file_index)
    # print(section_num)
    # print(list_user_name)
    # print(list_file_name)
    str_copy_version = ""

    if copy_version != 0:
        str_copy_version = "_"+str(copy_version)
    tmp_file_name = list_user_name[user_index] + "_" + str(list_file_name[file_index])


    left_hand_imu_unsync = list_of_folder_name[2]  +tmp_file_name + "_section"+ str(section_num)+ "_left_unsync"+str_copy_version+".txt"
    right_hand_imu_unsync = list_of_folder_name[4] + tmp_file_name + "_section"+ str(section_num)+ "_right_unsync"+str_copy_version+".txt"

    ear_imu = list_of_folder_name[0] + tmp_file_name + "_section" + str(section_num) + "_ear"+str_copy_version+".txt"
    left_hand_imu = list_of_folder_name[1] + tmp_file_name + "_section" + str(section_num) + "_left"+str_copy_version+".txt"
    right_hand_imu = list_of_folder_name[3] + tmp_file_name + "_section" + str(section_num) + "_right"+str_copy_version+".txt"

    video_imu = list_of_folder_name[5] + tmp_file_name + "_section" + str(section_num) +str_copy_version+".mp4"

    imu_info = list_of_folder_name[6] + tmp_file_name + "_section" + str(section_num) + "_imu_info"+str_copy_version+".txt"
    return [ear_imu,left_hand_imu,left_hand_imu_unsync,right_hand_imu,right_hand_imu_unsync,video_imu,imu_info]


def get_user_name(parent_path,user_index):
    file_user_name = open(parent_path + "/file_name_tracking/user_name.txt", "r")
    list_user_name = strip_lines(file_user_name.readlines())
    return list_user_name[user_index]

def get_video_list_file(user_name):
    video_list_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study/user_study_0208/user_slides/"+user_name+"/all_selected_videos.txt"
    return video_list_path

def update_user_file_index(list_user_file_index,parent_path):

    user_index = list_user_file_index[0]
    file_index = list_user_file_index[1]
    section_index = list_user_file_index[2]

    file_user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "w")
    user_name = get_user_name(parent_path, user_index)
    file_list_name = open(get_video_list_file(user_name), "r")
    size_of_file_list = len(file_list_name.readlines())

    if file_index == size_of_file_list - 1:
        user_index = user_index + 1
        file_index = -1

    file_user_file_index.write(str(user_index)+"\n")
    file_user_file_index.write(str(file_index)+"\n")
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

def get_list_of_file_name(parent_path,redo_status=0,copy_version = 0):  # confirms that the code is under main function

    experiment_result_parent_path = parent_path + "/experiment result/"

    user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "r")
    list_user_file_index = get_user_file_index(strip_lines(user_file_index.readlines()))

    file_user_name = open(parent_path+"/file_name_tracking/user_name.txt", "r")
    list_user_name = strip_lines(file_user_name.readlines())

    user_index = list_user_file_index[0]
    user_name = get_user_name(parent_path, user_index)

    file_file_name = open(get_video_list_file(user_name), "r")



    list_file_name = get_file_name(strip_lines(file_file_name.readlines()))
    user_index = list_user_file_index[0]

    if redo_status == 1:
        list_user_file_index[1] -=1

    print(list_user_file_index)
    # print(list_user_name)
    # print(list_file_name)

    # print("user_name:",list_user_name[list_user_file_index[0]])
    # print("sentence#:",list_file_name[list_user_file_index[1]])
    # print("secion#:",list_user_file_index[2])
    user_file_index.close()
    file_user_name.close()
    file_file_name.close()



    list_of_folder_name = create_folder(list_user_file_index,list_user_name,experiment_result_parent_path)
    list_of_file_name = generate_file_name(list_of_folder_name,list_user_file_index, list_user_name, list_file_name,copy_version)


    # if redo_status == 0:
    list_user_file_index[1] +=1

    # if redo_status ==2:
    #     pass

    update_user_file_index(list_user_file_index, parent_path)
    # for file_name in list_of_folder_name:
    #     print(file_name)
    #
    # print(" ")

    # for file_name in list_of_file_name:
    #     print(file_name)


    return list_of_file_name

def create_file_name_cali(list_user_file_index,list_user_name,parent_path):
    parent_path = parent_path + "/experiment result/cali/"

    section_path = parent_path + str(list_user_name[list_user_file_index[0]]) + "/synced/"
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    section_raw_path = parent_path  + str(list_user_name[list_user_file_index[0]]) + "/unsync/"
    if not os.path.exists(section_raw_path):
        os.makedirs(section_raw_path)

    user_cali_path = section_path +list_user_name[list_user_file_index[0]]+"_Section"+ str(list_user_file_index[2]) + "_cali"
    left_hand_imu = user_cali_path + "_left_synced.txt"
    right_hand_imu = user_cali_path + "_right_synced.txt"

    raw_user_cali_path = section_raw_path + list_user_name[list_user_file_index[0]] + "_Section" + str(
        list_user_file_index[2]) + "_cali"
    left_hand_imu_unsync = raw_user_cali_path + "_left_unsync.txt"
    right_hand_imu_unsync = raw_user_cali_path + "_right_unsync.txt"
    imu_info = raw_user_cali_path + "_imu_info.txt"

    list_of_file_name = [left_hand_imu,right_hand_imu]
    list_of_file_name_imu = [left_hand_imu_unsync,right_hand_imu_unsync,imu_info]
    return list_of_file_name+list_of_file_name_imu

def get_list_of_file_name_cali(parent_path):
    user_file_index = open(parent_path+"/file_name_tracking/file_index.txt", "r")
    file_user_name = open(parent_path+"/file_name_tracking/user_name.txt", "r")

    list_user_file_index = get_user_file_index(strip_lines(user_file_index.readlines()))
    list_user_name = strip_lines(file_user_name.readlines())
    print(list_user_file_index)
    return create_file_name_cali(list_user_file_index, list_user_name,parent_path)


if __name__ == "__main__":
    parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"
    # file_list = get_list_of_file_name_cali(parent_path)
    file_list = get_list_of_file_name(parent_path)
    for f in file_list:
        print(f)
    # get_list_of_file_name_cali()