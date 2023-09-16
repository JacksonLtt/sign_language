import os

def update_client_file_to_all_servers(file_name):
    path_to_local_file = "/Users/taitinglu/Documents/GitHub/Ring/mockup\ study/imu_finger_raspi/tcp_exam/"+file_name
    path_to_remote_file = "/home/pi/Desktop/tcp_exam"

    server1 = "raspberrypi1.local"
    server2 = "raspberrypi2.local"
    server3 = "raspberrypi3.local"
    server4 = "raspberrypi4.local"
    server5 = "raspberrypi5.local"


    server_list = [server1, server2, server3, server4, server5]
    for server in server_list:
        os.system("sshpass -p \"123456\" scp " + path_to_local_file + " pi@" + server + ":/home/pi/Desktop/tcp_exam/")
        print(file_name+" is passed to " + server)

    print("")

def update_client_to_one_server(file_name,server_name):
    path_to_local_file = "/Users/taitinglu/Documents/GitHub/Ring/mockup\ study/imu_finger_raspi/tcp_exam/" + file_name
    path_to_remote_file = "/home/pi/Desktop/tcp_exam"


    os.system("sshpass -p \"123456\" scp " + path_to_local_file + " pi@" + server_name + ":/home/pi/Desktop/tcp_exam/")
    print(file_name + " is passed to " + server_name)

    print("")

# update_client_file_to_all_servers("tcp_client2.py")
update_client_to_one_server("tcp_client2.py","raspberrypi5.local")
update_client_to_one_server("tcp_client2.py","raspberrypi4.local")