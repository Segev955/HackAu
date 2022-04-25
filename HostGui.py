from tkinter import Tk
from users import*
from main import *
def host_screen(user:User):
    home_screen = Toplevel(screen)
    home_screen.title("Home Page")
    home_screen.geometry("300x250")
    create_menu_bar(home_screen)