from tkinter import Tk
from users import*

def host_screen(user:User):
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title(f"Host {user.username}")