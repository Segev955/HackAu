from datetime import time
from socket import *
from threading import Thread

from users import *

# GLOBAL CONSTANTS
HOST = ''
PORT = 55000
ADDR = (HOST, PORT)
MAX_CONNETIONS = 10
BUFSIZ = 1024

# GLOBAL VARIABLES
u = Users()
onlines = []

# set up server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


class Online:
    def __init__(self, addr, sock, name=""):
        self.addr = addr
        self.sock = sock
        self.name = name

    def set_name(self, name):
        self.name = name
    def __repr__(self) -> str:
        return self.name


def date_from_str(date: str, spliter='/') -> tuple:
    tup = (int(date.split(spliter)[1]), int(date.split(spliter)[0]), int(date.split(spliter)[2]))
    return tup


def broadcast(msg):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return: None
    """
    for online in onlines:
        sock = online.sock
        try:
            sock.send(msg)
        except Exception as e:
            print("[EXCEPTION]", e)

def sendto(msg, name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return: None
    """
    for online in onlines:
        if online.name == name:
            sock = online.sock
            try:
                sock.send(msg)
            except Exception as e:
                print("[EXCEPTION]", e)




def client_communication(online: Online):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """
    client = online.sock

    # first message received is always the persons name
    name = client.recv(BUFSIZ).decode("utf8")
    online.set_name(name)

    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    while True:  # wait for any messages from person
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"):  # if message is qut - so disconnect the client
            onlines.remove(online)
            print(onlines)
        elif name == "HOME":
            if msg.split()[0] == "NEWUSER":
                user = User(username=msg.split()[1], password=msg.split()[2], gender=msg.split()[3], bdate=date_from_str(msg.split()[4]), type=msg.split()[5])
                f, msg = u.newuser(user)
                sendto(f"NEWUSER,{f},{msg}","HOME")

            elif msg.split()[0] == "CHECKTYPE":
                for i in u.p.values():
                    if msg.split()[1]== i.username:
                        if msg.split[2]== i.type():
                            sendto(f"CHECKTYPE,true", "HOME")
                        else:
                            sendto(f"CHECKTYPE,false", "HOME")
                        break
            else:
                sendto(f"unknown message to home.", "HOME")
        else:
            broadcast("unknown message.")


def wait_for_connection():
    """
    Wait for connecton from new clients, start new thread once connected
    :return: None
    """
    while True:
        try:
            sock, addr = SERVER.accept()  # wait for any new connections
            online = Online(addr, sock)  # create new person for connection
            onlines.append(online)
            print(onlines)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(online,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


def start_server():
    SERVER.listen(MAX_CONNETIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


def stop_server():
    SERVER.close()
start_server()
