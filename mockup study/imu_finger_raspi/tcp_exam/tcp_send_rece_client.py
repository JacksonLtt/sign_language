import socket
import threading
import sys
import time
# --- functions ---

def recv_msg():
    while True:
        recv_msg = s.recv(1024)
        if not recv_msg:
            sys.exit(0)
        recv_msg = recv_msg.decode()
        print(recv_msg)

def send_msg():
    while True:
        send_msg = input(str("Enter message: "))
        send_msg = send_msg.encode()
        s.send(send_msg)
        print("Message sent")

def send_msg_sequential():
    while True:
        s.send(b"hello from Client")
        print("message sent")
        time.sleep(20)
# --- main ---

# host = socket.gethostname()
# host = "Taitings-MacBook-Pro.local"
host = "10.0.0.94"
print("hostname:",host)
print("client_name:",socket.gethostname())
port = 65432

s = socket.socket()
s.connect((host, port))

print("Connected to the server")

message = s.recv(1024)
message = message.decode()
print(message)

# thread has to start before other loop
t = threading.Thread(target=recv_msg)
t.start()

send_msg_sequential()