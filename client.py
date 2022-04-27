import os
import sys
import threading
import time
import tkinter
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread, Lock
import pickle
from tkinter import simpledialog, Button, Menu, HORIZONTAL, scrolledtext
from tkinter.ttk import Entry, Progressbar








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

        # open tcp socket for client
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

        # sends name of client to the server
        self.send_message(self.name)
        self.lock = Lock()


    def acceptUser(self,flag,msg):
        pass
    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode('utf-8')
                print(f"client {self.name} received message:{msg}")

                if self.name =="HOME":
                    if msg.split(0)=="NEWUSER":
                        if msg.split(1)=='True':
                            pass



                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCPETION]", e)

                break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        try:
            self.client_socket.send(bytes(msg, "utf8"))
        except Exception as e:
            print(e)

    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
        self.client_socket.close()

Client("HHH")