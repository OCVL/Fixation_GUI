import socket
import select


class Client():
    def __init__(self, var):
        # get the instance of the variables class to pass to everything
        # self.var = variable_properties.Variables()
        # self.var.recvQ = recvQueue
        self.var = var
        self.client()
    def client(self):
        print("in the client")
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 65432  # The port used by the server
        FOV = '1'
        VIDNUM = '0'


        # instantiate a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('socket instantiated')

        # connect the socket
        connectionSuccessful = False
        while not connectionSuccessful:
            try:
                sock.connect((HOST,
                              PORT))  # Note: if execution gets here before the server starts up, this line will cause an error, hence the try-except
                print('socket connected')
                connectionSuccessful = True
            except:
                pass

        socks = [sock]
        while True:
            readySocks, _, _ = select.select(socks, [], [], 5)
            for sock in readySocks:
                message = self.receiveTextViaSocket(sock)
                if message:
                    message = message.decode()
                    print("recieved data")
                    parsed = message.split(";")
                    # extract data from message
                    if parsed[0] == FOV:
                        self.var.recvQ.put(message)
                    elif parsed[0] == VIDNUM:
                        self.var.recvQ.put(message)
                    else:
                        print("Client Shit hit the fan")
                print('received: ' + str(message))

    def receiveTextViaSocket(self, sock):
        ACK_TEXT = 'text_received'
        # get the text via the scoket
        message = sock.recv(1024)

        # if we didn't get anything, log an error and bail
        if not message:
            print('error: encodedMessage was received as None')
            return None

        # now time to send the acknowledgement
        # encode the acknowledgement text
        encodedAckText = bytes(ACK_TEXT, 'utf-8')
        # send the encoded acknowledgement text
        sock.sendall(encodedAckText)

        return message


if __name__ == '__main__':
    print("hi")
    # client()