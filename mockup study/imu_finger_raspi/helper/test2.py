import threading
import time
import keyboard
import read_file_name

command1 = b'-1'
command2 = b'-1'
command3 = b'-1'
command4 = b'-1'
command_last = b'-1'

last_command_remembered = False
sendcommand1 = False
sendcommand2 = False
sendcommand3 = False
sendcommand4 = False


def check_keyboard_press2():
    global command1
    global command2
    global command3
    global command4
    global command_last

    global sendcommand1
    global sendcommand2
    global sendcommand3
    global sendcommand4
    keep_track = True
    parent_path = "/Users/taitinglu/Documents/GitHub/Ring/mockup study"

    while True:
        while True:

            key_press = keyboard.read_key()
            command1 = bytes(str(key_press) + "\n", 'utf-8')
            command2 = command1
            command3 = command1
            command4 = command1
            if command1 == b's\n':
                read_file_name.get_list_of_file_name(parent_path,0)
            elif command1 == b'r\n':
                read_file_name.get_list_of_file_name(parent_path, 1)
            elif command1 == b'r\n':
                read_file_name.get_list_of_file_name(parent_path, 1)
            if command1!=b'e\n':
                command_last = command1


            print("you pressed",key_press)
            time.sleep(0.5)
            # print(time.time(), "command1:", command1)
            # print(time.time(), "command2:", command2)

            if key_press == "z":
                keep_track = False
            break

        sendcommand1 = True
        sendcommand2 = True
        sendcommand3 = True
        sendcommand4 = True
        # print(time.time(), "sendcommand1:", sendcommand1)
        # print(time.time(), "sendcommand2:", sendcommand2)
        if keep_track == False:
            break

count_copy = 0

if __name__ == "__main__":

    keyboard_detect_thread = threading.Thread(target=check_keyboard_press2)
    keyboard_detect_thread.start()
