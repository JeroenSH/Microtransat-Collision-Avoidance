from pyais import decode_raw
import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 10110

#setting up ports
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

keys = ['mmsi','lon','lat','speed','course','heading']
file = open("data.txt", "w")

for element in keys:
    file.write(element + ",")
file.write("\n")
i = 0
while i < 10:
    try:
        i +=1
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print("received message: %s" % data)
        decoded_data = decode_raw(data)
        print(decoded_data)
        selected_data = [decoded_data.get(key) for key in keys]
        print(selected_data)
        file.write(json.dumps(selected_data)+ "\n")
        print("\n")
    except:
        print("error")
file.close()
