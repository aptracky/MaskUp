## MASKUP - Authors: Andrew P, Mohamed B ##

# Imports
import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib
from threading import Thread
from PIL import Image

### PUT YOUR IP AND PORT HERE
HOST=''
PORT=
#############################
mouthCascade = cv2.CascadeClassifier("cascades/Mouth.xml")
THREADS = []

class ClientHandler(Thread):
    def __init__(self, addr, conn):
        Thread.__init__(self)
        self.addr = addr
        self.conn = conn
        print("[+] New Server socket thread started")

    def run(self):
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        while True:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += conn.recv(4096)

                print("Done Recv: {}".format(len(data)))
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
                print("msg_size: {}".format(msg_size))
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                mouths = mouthCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.3,
                    minNeighbors=8,
                    minSize=(6, 6)
                    )

                if (len(mouths) > 0):
                    send = "0"
                    conn.send(send.encode())
                    img = Image.open("assets/NETWORK2.PNG")
                    img.show("Image")
                else:
                    send = "1"
                    conn.send(send.encode())
                    img = Image.open("assets/NETWORK.PNG")
                    img.show("Image")

                
                for (x, y, w, h) in mouths:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                cv2.imshow('ImageWindow',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break




s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')

while True: 
    s.listen(10)
    print('Socket now listening')
    conn,addr=s.accept()
    newThread = ClientHandler(addr, conn)
    newThread.start()
    THREADS.append(newThread)

for t in THREADS:   
    t.join