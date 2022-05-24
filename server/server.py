from datetime import time
from socket import *
from threading import Thread
import time
from users import *
from objects import Meal, Meals

# GLOBAL CONSTANTS
HOST = ''
PORT = 55000
ADDR = (HOST, PORT)
MAX_CONNETIONS = 10
BUFSIZ = 1024

# GLOBAL VARIABLES
u = Users()
m=Meals()
onlines = []

# set up server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


class Online:
    global counter
    counter = 0

    def __init__(self, addr, sock, name=f"online{counter}"):
        self.addr = addr
        self.sock = sock
        self.name = name

    def set_name(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name


def date_from_str(date: str, spliter='/') -> tuple:
    lst = []
    print(date)
    lst.append(int(date.split(spliter)[1]))
    lst.append(int(date.split(spliter)[0]))
    lst.append(int(date.split(spliter)[2]))
    tup = [int(date.split(spliter)[1]), int(date.split(spliter)[0]), int(date.split(spliter)[2])]
    return lst


def time_from_str(time: str, spliter='/') -> tuple:
    lst = []
    print(time)
    lst.append(int(time.split(spliter)[1]))
    lst.append(int(time.split(spliter)[0]))
    tup = [int(time.split(spliter)[1]), int(time.split(spliter)[0])]
    return lst


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
            sock.send(bytes(msg, "utf8"))
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
                sock.send(bytes(f"{msg}", "utf8"))
            except Exception as e:
                print("[EXCEPTION]", e)


def get_online_index(name):
    for i in range(len(onlines)):
        if onlines[i].name == name:
            return i
    return None


def rename_client(online: Online, newname: str):
    sendto(f"RENAME,{newname}", online.name)
    # time.sleep(0.1)
    onlines.pop(get_online_index(online.name))
    online.name = newname
    onlines.append(online)
    # oldonline=get_online(oldname)
    # newonline=Online(oldonline.addr,oldonline.sock,newname)
    # onlines.remove(oldonline)
    # onlines.append(newonline)

def send_meals():
    m.load_from_json()
    while True:
        for meal in m.p.values():
            broadcast(f"MEAL,{meal.id},{meal}")
            time.sleep(0.1)
        time.sleep(10)
def client_communication(online: Online):
    """
    Thread to handle all messages from client
    :param person: Person
    :return: None
    """

    # first message received is always the persons name
    onlines.append(online)
    name = f"CLIENT~{len(onlines)}"
    rename_client(online, name)
    msg = f"{onlines[get_online_index(name)].name} has connected to the Server!"
    broadcast(msg)  # broadcast welcome message
    print(f"Online users: {onlines}")
    client = onlines[get_online_index(name)].sock
    Thread(target=send_meals).start()
    while True:  # wait for any messages from person
        msg = client.recv(BUFSIZ).decode("utf8")
        # time.sleep(1)
        sp = []
        try:
            sp = msg.split(',')
        except:
            break

        if msg == "{quit}":  # if message is qut - so disconnect the client
            onlines.remove(online)
            print(f"Online users: {onlines}")

        elif sp[0] == "NEWUSER":
            user = User(username=sp[1], password=sp[2], gender=sp[3], bdate=date_from_str(sp[4], '.'), type=sp[5])
            f, msg = u.newuser(user)
            sendto(f"NEWUSER,{f},{msg}", online.name)
        elif sp[0] == "CHECKTYPE":
            for i in u.p.values():
                if sp[1] == i.username:
                    if i.type == 'Host':
                        sendto(f"TYPE,{i.username},HOST", online.name)
                    else:
                        sendto(f"TYPE,{i.username},GUEST", online.name)
                    break
        elif sp[0] == "NEWMEAL":
            meal = Meal(host=online.name, title=sp[1], date=date_from_str(sp[2], '.'), time=time_from_str(sp[3],'.'), address=sp[4],
                        kosher=sp[5], capacity=sp[6], details=sp[7])
            f, msg = m.newmeal(meal)
            sendto(f"NEWMEAL,{f},{msg}", online.name)
        elif sp[0] == "CHECKTYPE":
            for i in u.p.values():
                if sp[1] == i.username:
                    if i.type == 'Host':
                        sendto(f"TYPE,{i.username},HOST", online.name)
                    else:
                        sendto(f"TYPE,{i.username},GUEST", online.name)
                    break
        elif sp[0] == "CHECKPASS":
            f, msg = u.chekcpass(sp[1], sp[2])
            sendto(f"CHECKPASS,{f},{msg}", online.name)
        elif sp[0] == "RENAME":
            rename_client(onlines[get_online_index(sp[1])], sp[2])

        elif msg == "USERTOSTRING":
            if online.name in u.p.keys():
                sendto(f"USERTOSTRING,{u.p[online]}", online.name)

        else:
            print(f"Unknown Message: {msg}")


def wait_for_connection():
    """
    Wait for connecton from new clients, start new thread once connected
    :return: None
    """
    while True:
        try:
            sock, addr = SERVER.accept()  # wait for any new connections
            online = Online(addr, sock)  # create new person for connection

            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[CONNECTION] {addr} connected to the server at {now}")
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
