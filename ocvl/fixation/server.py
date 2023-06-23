import sys
from queue import Queue

def server():
    # echo-server.py

    import socket

    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    time_out = 2
    FOV = b"0"
    VIDNUM = b"1"
    recvQ = Queue(0)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        s.setblocking(False)

        with conn:
            print(f"Connected by {addr}")
            while True:
                # ready = select.select([s], [], [], time_out)
                # if ready[0]:
                data = conn.recv(1024)
                # print(sys.getsizeof(data))
                if data:
                    print(f"Received {data!r}")  # prints what was recieved here from the client
                    parsed = data.split(b",")
                    print(parsed[0])
                    # extract data from message
                    if parsed[0] == FOV:
                        recvQ.put(data.decode())
                        # recvQ.put((parsed[1].decode(), parsed[2].decode()))
                        print(recvQ.get())
                    elif parsed[0] == VIDNUM:
                        recvQ.put(data.decode())
                        print(recvQ.get())
                    else:
                        print("Shit hit the fan")
                    conn.sendall(data)  # sends message it recieved back to the client

                if sys.getsizeof(data) == 33:  # 33 is 0 bytes (what is received when the client dies/is closed)
                    s.close()
                    break

if __name__ == "__main__":
    server()