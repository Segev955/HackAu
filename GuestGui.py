from tkinter import Tk

import main
from users import*

def guest_screen(user:User):
    main.create_menu_bar()
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title(f"Guest {user.username}")