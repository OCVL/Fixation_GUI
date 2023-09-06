import logging
import os
import subprocess
import threading
import time
import platform
import socket
# for python2.7
from Queue import Queue
# for python3
# from queue import Queue


class FixGUIServer:
    def __init__(self, sendQueue=None):
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

        self.serverThread = threading.Thread(target=Server, args=(sendQueue, self))
        # self.serverThread.daemon = True
        self.serverThread.start()



class Server:
    def __init__(self, sendQueue, FixGUIServerRef):

        self._sendQueue = sendQueue
        self._fixGuiServerRef = FixGUIServerRef

        print("in the server class")

        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        # instantiate a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')

        # bind the socket
        sock.bind((HOST, PORT))
        print('socket binded')

        # start the socket listening
        sock.listen(1)
        print('socket now listening')

        # accept the socket response from the client, and get the connection object
        conn, addr = sock.accept()  # Note: execution waits here until the client calls sock.connect()
        print('socket accepted, got connection object')

        myCounter = 0
        while True:

            # if the main gui subprocesses was killed, close the socket, break the loop, and end. There will be a short delay before socket is closed
            if self._fixGuiServerRef.mainGUI.poll() is not None:
                sock.close()
                break
            elif sendQueue.qsize() > 0:
                message = sendQueue.get()

                print(message)
                print('sending')
                self.sendTextViaSocket(message, conn)
                # time.sleep(3)


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

    # first item in tuple contains key to if the message is an FOV or Video number
    FOV = 0
    VIDNUM = 1

    server = FixGUIServer(testQ)
    time.sleep(2)
    print("Starting test packets...")
    testQ.put(b"(0,1.0,1.0)")
    time.sleep(3)
    testQ.put(b"(1,0)")
    time.sleep(3)
    testQ.put(b"(0,2.0,2.0)")
    time.sleep(3)
    testQ.put(b"(1,1)")
    time.sleep(3)
    testQ.put(b"(0,1.0,1.0)")
    time.sleep(3)
    testQ.put(b"(1,2)")


