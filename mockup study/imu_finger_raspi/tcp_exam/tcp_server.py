# echo-server.py
import socket
import paramiko
import time
import sys
import threading
import keyboard
import sshkeyboard
import asyncio



class TCPServer:
    def __init__(self):
        self.Host = socket.gethostname()
        self.Host = "10.0.0.94"
        self.Port = 65432
        self.TCPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.TCPServerSocket = socket.socket()
        self.time_count = 100
        self.count = 0

        self.ble_request_send = False


        print("hostname:", self.Host)
        self.TCPServerSocket.bind((self.Host, self.Port))
        self.TCPServerSocket.listen()
        self.conn, self.addr = self.TCPServerSocket.accept()
        print("Client {} has connected".format(self.addr))

        try:
            t1 = threading.Thread(target=self.recv_msg)
            t1.start()
            t2 = threading.Thread(target=self.send_msg_sequential)
            t2.start()
            t3 = threading.Thread(target=self.check_keyboard_press)
            t3.start()
        except:
            # print(e)
            sys.exit()
        # while True:
        #     if self.count == 30:
        #         self.conn.shutdown(1)
        #         self.conn.close()
        #         self.TCPServerSocket.shutdown(1)
        #         self.TCPServerSocket.close()
        #         print("connection close")
        #         break

    def recv_msg(self):
        while True:
            if self.count == self.time_count:
                print("recv_msg close")
                break
            recv_msg = self.conn.recv(1024)
            if not recv_msg:
                sys.exit(0)
            recv_msg = recv_msg.decode()
            print(recv_msg)
            # if recv_msg[:10] == "connect to ":
            #     self.ble_start = True

    def check_keyboard_press(self):
        while True:
            keyboard.wait('space')
            if self.ble_request_send == False:
                print("ble start request send")
                self._helper_send_message("connect_ble")
                self.ble_request_send = True
            else:
                print("ble stop request send")
                self._helper_send_message("stop_ble")
                self.ble_request_send = False

    def send_msg(self):
        while True:
            send_msg = input(str("Enter message: "))
            send_msg = send_msg.encode()
            self.conn.send(send_msg)
            print("message sent")

    def send_msg_sequential(self):
        while True:
            if self.count == self.time_count:
                self.conn.shutdown(1)
                self.conn.close()
                # self.TCPServerSocket.shutdown(1)
                # self.TCPServerSocket.close()
                # self.off_server()
                break

            # if self.count in [2,7,12,17,23,28,33,38,43,48,53,58,64,69,76]:
            #     # self.conn.send(b'connect_ble')
            #     pass
            # else:
            #
            #     message = "hello from Server " + str(self.count)
            #     message = message.encode('utf-8')
                # print(time.perf_counter(),":message sent:", message)
                # self.conn.send(message)


            time.sleep(5)
            self.count += 1

    def off_server(self):
        self.TCPServerSocket.close()

    def _helper_send_message(self,message):
        message = message.encode('utf-8')
        self.conn.send(message)


if __name__ == "__main__":
    TCPServer1 = TCPServer()


