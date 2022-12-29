import os
from datetime import datetime
from node.ser_auth import *
from server.upload import *

# Public variable
total_port = 99
node_id = "none"
node_usb = 99
ser_baudrate = 115200

# Create message cache folder
cache_folder = "./cache"
isExist = os.path.exists(cache_folder)
if isExist == False:
    os.makedirs(cache_folder)

# Search connected node by serial com
for i in range(total_port):
    usb = os.system("ls /dev/ttyUSB{}".format(i))
    
    if usb == 0:
        get_node_id = ser_node(i, "ttyUSB", ser_baudrate)
        if len(get_node_id) == 6:
            node_id = get_node_id
            node_usb = i
            break
        
# Set detected node as LoRa receiver
print("Setup gateway with ", node_id, "\n")
print("Please wait . . .\n")
time.sleep(1)

print("Gateway is ready")

# Serial com
# send and receive data to main arduino
ser_node = serial.Serial(
   port='/dev/ttyUSB{}'.format(node_usb),
   baudrate = ser_baudrate,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)
ser_node.flush()
time.sleep(0.25)

# Collect data from LoRa node
while True:
    if ser_node.inWaiting():
        # get node id
        answer = ser_node.readline()
        decode_answer = answer.decode('utf-8')
        ser_node.flushInput()
        
        # Save to cache
        f = open("./cache/msg_log.txt","a")
        dt = datetime.now()
        f.write("{} \t".format(dt))
        f.write("{}\r\n".format(decode_answer))
        f.close()
    
        # Upload to firebase database
        if decode_answer.count("|") == 2:
            print(decode_answer)
            get_payload = decode_answer.split("|")
            sender = get_payload[0]
            path = get_payload[1]
            if get_payload[2].count(",") == 1:
                msg_data = get_payload[2].split(",")
                
                up_server(sender, "path", path)
                up_server(sender, "suhu", msg_data[0])
                up_server(sender, "kelembaban", msg_data[1])
