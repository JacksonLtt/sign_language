import socket
import sys
from _thread import start_new_thread
import threading
import time
HOST = '10.0.0.94' # all availabe interfaces
PORT = 65432 # arbitrary non privileged port
import keyboard

count = 0
keyboard_detect = False
message_command = ""
start_request = False
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except socket.error as msg:
    print("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
print("Listening...")

# The code below is what you're looking for ############

def client_thread(conn,addr):
    conn.send(b"Welcome to the Server. Type messages and press enter to send.\n")
    send_thread = threading.Thread(target=_helper_client_send_thread, args=(conn,))
    send_thread.start()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        reply = data.decode('utf-8')
        print("\t:",addr, ":", reply)
    conn.close()


def _helper_client_send_thread(conn):
    global count
    global keyboard_detect
    global message_command
    while True:
        if keyboard_detect == True:
            message = message_command.encode("utf-8")
            conn.sendall(message)
            time.sleep(1)
            count +=1
            keyboard_detect = False

def _helper_main_thread_keyboard():
    global keyboard_detect
    global message_command
    global  start_request
    while True:
        keyboard.wait('space')

        if start_request == False:
            message_command = "connect_ble"
            start_request = True
            print("\n\n[+] START request sent")
        else:
            message_command = "stop_ble"
            start_request = False
            print("\n\n[+] STOP request sent")

        keyboard_detect = True
        time.sleep(1)
        
def _helper_find_imu_name(addr):
    if addr == "10.0.0.160":
        return "ear"
    elif addr == "10.0.0.96":
        return "left"
    elif addr == "10.0.0.135":
        return "right"
    elif addr == "10.0.0.201":
        return "right"
    elif addr == "10.0.0.139":
        return "left"

    return -1


keyboard_detect_thread = threading.Thread(target=_helper_main_thread_keyboard)
keyboard_detect_thread.start()

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":"+_helper_find_imu_name(addr[0]) )

    start_new_thread(client_thread, (conn,addr,))

s.close()