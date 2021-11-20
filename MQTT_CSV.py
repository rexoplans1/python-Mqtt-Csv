from os import device_encoding
import serial
import typing
import csv
from paho.mqtt import client as paho
from serial.tools import list_ports
from typing import Union

from serial.tools.list_ports_common import ListPortInfo
from serial.tools.list_ports_windows import get_parent_serial_number

broker = "31.220.62.152"  # server id
port = 1883  # port numarası
baud = 9600  # stm runs at 9600 baud
fil_name = "analog-data.csv"  # name of the CSV file generated file_name
samples = 100  # alınacak örnek adedi
print_labes = False
timeout = 1

# Port ve port bilgilerini veren fonksiyon .
def print_devices() -> None:
    ports = list_ports.comports()

    for i, port in enumerate(ports):
        print(f"{i+1}. Port\n{'='*25}")
        print("description: ", port.description)
        print("name: ", port.name)
        print("device: ", port.device)
        print("hwid: ", port.hwid)
        print("interface: ", port.interface)
        print("location: ", port.location)
        print("manufacturer: ", port.manufacturer)
        print("usb_description: ", port.usb_description())
        pass


# Port ve port bilgilerini veren fonksiyon .
def find_device(device_name: str) -> Union[str, None]:
    ports = list_ports.comports()

    for port in ports:
        if device_name.lower() in port.description.lower():
            return port.usb_description()

        return None


print_devices()

arduino_port = find_device("ch340")
if arduino_port == find_device("ch340"):
    ser = serial.Serial(str(arduino_port), baudrate=9600)

    ("Connected to Stm port:" + arduino_port)
    file = open(fil_name, "a")
    print("Created file")
    line = 0

    def on_publish(client, userdata, result):  # create function for callback
        print("data yayinlandi")

    client1 = paho.Client("oda")  # create client object
    client1.on_publish = on_publish  # assign function to callback
    client1.connect(broker, port)  # establish connection

    while True:
        if print_labes:
            if line == 0:
                print("Line" + str(line) + " :wrting...")
            else:
                print("Line " + str(line) + ":writing...")
        getData = str(ser.readline().decode("utf-8"))[:-2]

        print(
            "gelen veri " + getData,
            f"{repr(getData[0])} | {repr(getData[-2])}  |{repr(getData[-1])}",
        )

        if getData.startswith("?") and getData[-1].endswith("#"):
            data = getData[1:-1]

            data = list(data.split(";"))
            FLAG = True

        else:
            FLAG = False

        if FLAG:
            print("mesaj yazildi")
            ret_msg = [client1.publish(f"oda/Cells{i+1}", data[i]) for i in range(10)]
            file = open(fil_name, "a")  # append the data to the file
            file.write(",".join(data) + "\n")  # write data with a newline
            line = line + 1
            print("Data collection complete!")
            ## clode file
            file.close()
else:
    print("Connection Issue!")
    quit()

print("DONE")
