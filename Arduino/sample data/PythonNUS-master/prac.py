from bleak import BleakClient, discover, BleakError
import asyncio
import struct
from functools import partial

count_left = 0
count_right = 0

UART_TX_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for TX
UART_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e" #Nordic NUS characteristic for RX
# UART_RX_UUID = "1234"

MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"
# MODEL_NBR_UUID = "1234"

def unpack_f_bytearray(bytearray):
    f_data = struct.unpack('f', bytearray)
    return f_data[0]

def unpack_l_bytearray(bytearray):
    l_data = struct.unpack('l', bytearray)
    return l_data[0]

# def decode_byte_data(bytedata):
#     float_array = []
#     for i in range(int(len(bytedata)/4)-2):
#
#         tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
#         float_array.append(tmp_float)
#
#     # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 8:-4] + bytes([0, 0, 0, 0]))) # macos struct.error: unpack requires a buffer of 8 bytes
#     # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:] + bytes([0, 0, 0, 0]))) # macos struct.error: unpack requires a buffer of 8 bytes
#     # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 8:-4] ))  # windows struct.error: unpack requires a buffer of 4 bytes
#     float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:])) # windows struct.error: unpack requires a buffer of 4 bytes
#     return float_array

def decode_byte_data(bytedata):
    float_array = []
    for i in range(int(len(bytedata)/4)):

        tmp_float = unpack_f_bytearray(bytedata[i*4:i*4+4])
        float_array.append(tmp_float)

    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 8:-4] + bytes([0, 0, 0, 0]))) # macos struct.error: unpack requires a buffer of 8 bytes
    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:] + bytes([0, 0, 0, 0]))) # macos struct.error: unpack requires a buffer of 8 bytes
    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 8:-4] ))  # windows struct.error: unpack requires a buffer of 4 bytes
    # float_array.append(unpack_l_bytearray(bytedata[len(list(bytedata)) - 4:])) # windows struct.error: unpack requires a buffer of 4 bytes
    return float_array


def callback(sender, data):
    global count_right
    count_right += 1
    # print(count_left, ",", data)
    # print(sender,",",data,",",unpack_f_bytearray(data))
    # print("size: ",len(data.decode())+1,"decoder: ",data.decode())
    result = decode_byte_data(data)
    print(len(result),":",count_right,":",result)
    f.write(str(result) + "\n")


    # global f
    # if result[-1] == 0:
    #     # print("left count: ", count_left, "result", result)
    #     print("left count: ", count_left)
    #     count_left += 1
    #
    # if result[-1] ==1:
    #     # print("right count: ", count_right, "result", result)
    #     print("right count: ", count_right)
    #     f.write(str(result[:-1]) + "\n")
    #     count_right += 1

def my_notification_callback_with_client_input(client: BleakClient, sender: int, data: bytearray):
    """Notification callback with client awareness"""
    print(client.address,":",data)
    result = struct.unpack('l', data + bytes([0, 0, 0]))[0]

    global count_left
    global count_right
    if result == 0:
        print(sender, ": left count: ", count_left, "result", result)
        count_left += 1

    if result == 1:
        print(sender, ": right count: ", count_right, "result", result)
        count_right += 1

def disconnect_callback(client):
    print("Client with address {} got disconnected!".format(client.address))

def run_connect(addresses):
    loop = asyncio.get_event_loop()

    tasks = asyncio.gather(
        *(connect_to_device(address, loop) for address in addresses)
    )

    loop.run_until_complete(tasks)

async def connect_to_device(address, loop):

    async with BleakClient(address[0], loop=loop) as client:

        print("connect to ", address)
        try:
            # x = await client.is_connected()
            # print("Connected: {0}".format(x))
            await client.start_notify(UART_RX_UUID, callback)
            # await client.start_notify(UART_RX_UUID,  partial(my_notification_callback_with_client_input, client))
            await asyncio.sleep(40)

            await client.stop_notify(UART_RX_UUID)
            print("end")


        except Exception as e:
            print(e)

    print("disconnect from", address)

# f = open("C:/Users/txl5518/Documents/Github/sign_language/Arduino/sample data/PythonNUS-master/7.txt",'w',newline='')
# f = open("C:/Users/Taiting/Documents/GitHub/sign_language/Arduino/sample data/PythonNUS-master/10.txt",'w',newline='')
# f = open("/Users/taitinglu/Documents/GitHub/sign_language/Arduino/sample data/PythonNUS-master/4.txt",'w',newline='')
# f = open("C:/Users/Taiting/Documents/GitHub/sign_language/Arduino/sample data/PythonNUS-master/10.txt",'w',newline='')
f = open("/Users/taitinglu/Documents/GitHub/sign_language/Arduino/sample data/PythonNUS-master/4.txt",'w',newline='')

if __name__ == "__main__":
    # addresses = [("D8:A0:1D:5D:7E:FE", "right_hand")]
    # addresses = [("A4:E5:7C:C0:04:E2","left_hand")]
    # addresses = [("D8:A0:1D:5D:7E:FE","right_hand"),("A4:E5:7C:C0:04:E2","left_hand")]

    # addresses = [("50:02:91:A1:AA:32","left_hand")]
    # addresses = [("50:02:91:A1:A7:5A", "right_hand")]
    # addresses = [("50:02:91:A1:A7:5A", "right_hand"), ("50:02:91:A1:AA:32", "left_hand")]
    addresses = [('9C211E49-F2B3-45CE-B691-9B13D58217C9',"right hand"),('E08FC2D4-E70E-42B0-A767-07A6F555736C','left hand')]
    addresses = [("E93C311A-B0A3-41C3-800C-4B5B541FC782","Feather nRF52832")]
    addresses = [("22020732-46A7-4F91-B01D-8423CC584C1E","Feather nRF52832")]
    addresses = [("C8:B3:A4:26:46:8F", "nRF52832 Button")]
    addresses = [("F45E7C56-20A1-487C-AA49-9137616CFF97", "nRF52832 Button")]
    # addresses = [('AC:67:B2:36:82:BE',"left hand")]
    # addresses = [("EF504132-F2ED-4D69-B0A5-731DCA06D098", "BatteryMonitor")]


    run_connect(addresses)
    f.close()
    print("left count: ",count_left)
    print("right count: ",count_right)

