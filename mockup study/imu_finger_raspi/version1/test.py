import asyncio
import time
import keyboard
from sshkeyboard import listen_keyboard
import paramiko

def test_listen_sshkeyboard():
    global detect_z
    detect_z= False

    def press(key):
        print(f"'{key}' pressed")
        # global  detect_z
        # if key == "z":
        #     print("detect:",key)
        #     detect_z = True
        #     print("detect:", detect_z)

    print("start listen")
    while True:
        print("while detect_z",detect_z)
        listen_keyboard(on_press=press,until="z")
        # print("end listen detect_z", detect_z)
        # if detect_z == True:
        break

    print("Final detect z")




hostname = "10.0.0.96"
username = "pi"
password = "123456"

command_run_peripheral = "sudo python3 /home/pi/Desktop/ASL/data_process/tmp_peripheral.py"
# command_run_peripheral = "sudo python3 /home/pi/Desktop/ASL/data_process/test_1.py"
# initialize the SSH client
client = paramiko.SSHClient()
# add to known hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=hostname, username=username, password=password)

except:
    print("[!] Cannot connect to the SSH Server")
    exit()

# console = client.invoke_shell()
# console.keep_this = client
# print(console)
# execute the commands
# for command in commands:
print("="*5, command_run_peripheral, "="*50)
stdin, stdout, stderr = client.exec_command(command_run_peripheral)
count =1
start_time = time.perf_counter()
while True:
    if stdout.channel.recv_ready() and count ==1:
        start_time = time.perf_counter()
        print(start_time,":",stdout.channel.recv(1024).decode())
        count +=1
        # break

        # time.sleep(0.01)
    elif stdout.channel.recv_ready() and count == 2:
        time.sleep(5)
        stdin.write("z\n")
        stdin.flush()
        print(time.perf_counter(), ":", stdout.channel.recv(1024).decode())
        count+=1


    else:
        if keyboard.is_pressed("q"):
            # print("STOP connect to ")
            stdin.write("z\n")
            stdin.flush()
            print(time.perf_counter() - start_time, "\n:", stdout.channel.recv(1024).decode())


# stdin.write("user" + '\n')
# stdout.flush()
# # print(stdout)






