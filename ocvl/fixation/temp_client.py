# client.py
import time
import socket
import select

class Client():
    def __init__(self, parent=None):
        self.client()
    def client(self):
        print("in the client")
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server
        message = 1
        time_out = 2
        packet = b"(0,1.0,1.0)"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.setblocking(False)
            while True:
                s.sendall(packet)
                # s.sendall(message.to_bytes(1, byteorder='big'))
                ready = select.select([s], [], [], time_out)
                if ready[0]:
                    data = s.recv(1024)
                    print(f"Received {data!r}")
                message += 1
                time.sleep(2)
                if message > 5:
                    s.close()
                    break




if __name__ == '__main__':
    print("hi")
    # client()