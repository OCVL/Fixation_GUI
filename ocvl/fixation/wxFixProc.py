import asyncio
import datetime
import logging
import os
import subprocess
import datetime
import sys
import threading
import time
import socket
import platform
from queue import Queue

import select
import variable_properties
import pickle


class FixGUIServer:
    def __init__(self, recvQueue=None):
        # get the instance of the variables class to pass to everything

        self.var = variable_properties.Variables()
        self.var.recvQ = recvQueue
        logging.basicConfig(filename='fixGUIServer.log', level=logging.DEBUG)
        thispath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        if platform.system() == 'Windows':
            py3path = os.path.join(thispath[:-4], 'venv', 'Scripts', 'pythonw.exe')
        else:
            py3path = os.path.join(thispath, 'venv', 'bin', 'python3')
        guipath = os.path.join(thispath, 'fixation', 'nuclear_base.py')
        print('Launching the Fixation GUI at ' + py3path)
        print('guipath: ' + guipath)

        # myList = [self.var]
        self.mainGUI = subprocess.Popen([py3path, guipath])
        time.sleep(2)



        self.server = Server(self.var)
        # self.serverThread = threading.Thread(target=Server, args=(self.var,))
        # self.serverThread.daemon = True
        # self.serverThread.start()




class Server:
    def __init__(self, var):
        self.var = var

        self.server()

    def server(self):
        # echo-server.py

        import socket

        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        time_out = 2
        FOV = b"(0"
        VIDNUM = b"(1"

        print("in the server")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            s.setblocking(False)

            with conn:
                print(f"Connected by {addr}")
                while True:
                    print("in while")
                    # ready = select.select([s], [], [], time_out)
                    # if ready[0]:
                    data = conn.recv(1024)
                    # print(sys.getsizeof(data))
                    if data:
                        print("recieved data")
                        self.var.recvQ.put(data.decode())
                        print(data.decode())
                        print(self.var.recvQ)
                        # # print(f"Received {data!r}")  # prints what was recieved here from the client
                        # parsed = data.split(b",")
                        # # print(parsed[0])
                        # # extract data from message
                        # if parsed[0] == FOV:
                        #     self.var.recvQ.put(data.decode())
                        #     # recvQ.put((parsed[1].decode(), parsed[2].decode()))
                        #     # print(self.var.recvQ.get())
                        # elif parsed[0] == VIDNUM:
                        #     self.var.recvQ.put(data.decode())
                        #     # print(self.var.recvQ.get())
                        # else:
                        #     print("Shit hit the fan")
                        conn.sendall(data)  # sends message it recieved back to the client

                    if sys.getsizeof(data) == 33:  # 33 is 0 bytes (what is received when the client dies/is closed)
                        s.close()
                        break



if __name__ == '__main__':

    testQ = Queue()

    server = FixGUIServer(testQ)

