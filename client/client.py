import sys
import time
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread

class Client:
    """
    for communication with server
    """
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    else:
        HOST = '127.0.0.1'
    PORT = 55000
    ADDR = (HOST, PORT)
    BUFSIZ = 1024
    def __init__(self,name="HOME"):
        """
        Init object and send name to server
        :param name: str
        """
        self.name=name
        self.isconnected=False
        tcp_thread = Thread(target=self.tcp_connection)
        tcp_thread.start()


        # self.lock = Lock()

    def tcp_connection(self):
        while True:
            if not self.isconnected:
                try:

                    # open tcp socket for client
                    self.client_socket = socket(AF_INET, SOCK_STREAM)
                    self.client_socket.connect(self.ADDR)
                    self.messages = ["messages:"]
                    self.isconnected = True
                    receive_thread = Thread(target=self.receive_messages)
                    receive_thread.start()

                    # sends name of client to the server
                    self.send_message("New Client Connected Successfully.")
                    print(f"Connected to the Server with Client name {self.name}")

                except:
                    pass



    def acceptUser(self,flag,msg):
        pass
    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            if self.isconnected:
                try:
                    msg = self.client_socket.recv(self.BUFSIZ).decode('utf-8')
                    sp=[]
                    print(f"{self.name} received message: {msg}")
                    try:
                        sp=msg.split(',')
                        if sp[0] =="RENAME":
                            self.name=sp[1]
                            print(f"Client Name changed to {self.name}")
                    except:
                        pass

                    # make sure memory is safe to access
                    # self.lock.acquire()
                    self.messages.append(msg)
                    # self.lock.release()
                except Exception as e:
                    print("[EXCPETION]", e)
                    pass

                    break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        try:
            self.client_socket.send(bytes(f"{msg}", "utf8"))
            return True
        except Exception as e:
            self.disconnect()
            return False

    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        # self.lock.acquire()
        # self.messages = []
        # self.lock.release()

        return messages_copy

    def disconnect(self):
        try:
            self.send_message("{quit}")
        except:
            print("The Server is crushed.")
        self.isconnected=False
        self.client_socket.close()

# cl=Client("HOME")
# time.sleep(0.1)
# cl.send_message(f"CHECKTYPE,aaaaaa")
# cl.send_message(f"NEWUSER,dasssasdas,12345678,male,1-3-1998,HOST")
# time.sleep(0.1)
# print(cl.get_messages()[-1])
# time.sleep(0.1)
# cl.send_message(f"CHECKTYPE,salishar")
# time.sleep(0.1)
# print(cl.get_messages()[-1])
# cl.send_message(f"CHECKTYPE,aaaaaa")
# time.sleep(0.1)
# cl.send_message(f"CHECKTYPE,aaaaaa")
# time.sleep(0.1)
# cl.send_message(f"NEWUSER,dasssasdas,12345678,male,1-3-1998,HOST")
# cl.send_message(f"CHECKTYPE,aaaaaa")
# cl.send_message(f"CHECKPASS,salishar,12345678")
# print(cl.get_messages()[-1])
# time.sleep(0.1)
# print(cl.get_messages()[-1])