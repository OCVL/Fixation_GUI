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
import socket



class FixGUIServer:
    def __init__(self, recvQueue=None):
        # get the instance of the variables class to pass to everything

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



        # self.server = Server()
        self.serverThread = threading.Thread(target=Server)
        # self.serverThread.daemon = True
        self.serverThread.start()




class Server:
    def __init__(self):


        self.server()

    def server(self):
        print("in the server")

        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        m = 0
        packet = [b"(0,2.0,2.0)", b"(1,0)"]
        # b"(0,2.0,2.0)", b"(1,0)", b"(0,1.0,1.0)", b"(1,1)", b"(0,2.0,2.0)", b"(0,3.0,3.0)"

        # instantiate a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')

        # bind the socket
        sock.bind((HOST, PORT))
        print('socket binded')

        # start the socket listening
        sock.listen()
        print('socket now listening')

        # accept the socket response from the client, and get the connection object
        conn, addr = sock.accept()  # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')

        myCounter = 0
        while True:
            if m < len(packet):
                message = (packet[m])
                print('sending')
                self.sendTextViaSocket(message, conn)
                m += 1
                time.sleep(3)
                if m > len(packet)-1:
                    sock.close()
                    break

    def sendTextViaSocket(self, message, sock):
        ACK_TEXT = 'text_received'

        # send the data via the socket to the server
        sock.sendall(message)

        # receive acknowledgment from the server
        encodedAckText = sock.recv(1024)
        ackText = encodedAckText.decode('utf-8')

        # log if acknowledgment was successful
        if ackText == ACK_TEXT:
            print('server acknowledged reception of text')
        else:
            print('error: server has sent back ' + ackText)


if __name__ == '__main__':

    testQ = Queue()

    server = FixGUIServer(testQ)

