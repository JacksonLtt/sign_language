import socket
import threading
import sys

# --- functions ---
import time


def recv_msg():
    while True:
        recv_msg = conn.recv(1024)
        if not recv_msg:
            sys.exit(0)
        recv_msg = recv_msg.decode()
        print(recv_msg)

def send_msg():
    while True:
        send_msg = input(str("Enter message: "))
        send_msg = send_msg.encode()
        conn.send(send_msg)
        print("message sent")


def send_msg_sequential():
    while True:
        message = str("hello from Server")
        conn.send(b"hello from Server")
        print("message sent")
        time.sleep(5)
# --- main ---

host = socket.gethostname()
host = "10.0.0.94"
port = 65432

s = socket.socket()
print("hostname:",host)
s.bind((host, port))
s.listen()

print("Waiting for connections")
conn, addr = s.accept()

print("Client has connected")
conn.send("Welcome to the server".encode())

# thread has to start before other loop
t = threading.Thread(target=recv_msg)
t.start()

send_msg_sequential()