from tkinter import Tk
from users import*

def guest_screen(user:User):
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title(f"Guest {user.username}")