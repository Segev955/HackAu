import datetime
import tkinter.messagebox
import urllib
import webbrowser
from tkinter import *
from tkcalendar import Calendar

import GuestGui
import HostGui
from users import *

u = Users()


def date_from_str(date:str,spliter='/')->tuple:
    print(date)
    if date is None or len(date.split(spliter))!=3:return None
    tup= (int(date.split(spliter)[1]) ,int(date.split(spliter)[0]) ,int(date.split(spliter)[2]))
    return tup
def getGender(g:int):
    match(g):
        case 0:
            return "male"
        case 1:
            return "female"
        case 2:
            return "other"
def getType(t:int):
    match(t):
        case 0:
            return "Host"
        case 1:
            return "Guest"
def singup(screen,username: str, password: str, gender: str, bdate, type: int):
    user = User(username=username, password=password, gender=gender, bdate=bdate, type=type)
    f, msg = u.newuser(user)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen,user)
    else:
        tkinter.messagebox.showerror(message=msg)


def login(screen,username, password):
    f, msg = u.chekcpass(username=username, password=password)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen,User(username=username, password=password, gender=u.p[username][2], bdate=u.p[username][3], type=u.p[username][4]))
    else:
        tkinter.messagebox.showerror(message=msg)
def open_user_win(screen,user):
    screen.destroy()
    if user.type == "Host":
        HostGui.host_screen(user)
    else:
        GuestGui.guest_screen(user)


def register():
    reg_screen = Toplevel(screen)
    reg_screen.title("Register")
    reg_screen.geometry("700x700")

    username = StringVar()
    password = StringVar()
    gender = IntVar()
    type = IntVar()

    Label(reg_screen, text="Please enter").pack()
    Label(reg_screen, text=" ").pack()
    Label(reg_screen, text="Username: ").pack()
    Entry(reg_screen, textvariable=username).pack()
    Label(reg_screen, text="Password: ").pack()
    Entry(reg_screen, textvariable=password, show="*").pack()
    Label(reg_screen, text="Gender: ").pack()
    Radiobutton(reg_screen, text="male", variable=gender, value=0).pack()
    Radiobutton(reg_screen, text="female", variable=gender, value=1).pack()
    Radiobutton(reg_screen, text="other", variable=gender, value=2).pack()
    Label(reg_screen, text="Date of birth: ").pack()
    m,y,d=date_from_str(str(datetime.date.today()),'-')
    cal=Calendar(reg_screen, year=y, month=m, day=d)
    cal.pack()
    Radiobutton(reg_screen, text="Host", variable=type, value=0).pack()
    Radiobutton(reg_screen, text="Guest", variable=type, value=1).pack()
    Label(reg_screen, text=" ").pack()


    Button(reg_screen, text="Register", width=30, height=2,
           command=lambda: singup(reg_screen,username.get(),password.get(),getGender(gender.get()),date_from_str(cal.get_date()),getType(type.get())) in ()).pack()


def connect():
    log_screen = Toplevel(screen)
    log_screen.title("Login")
    log_screen.geometry("300x250")

    username = StringVar()
    password = StringVar()

    Label(log_screen, text="Please enter").pack()
    Label(log_screen, text=" ").pack()
    Label(log_screen, text="Username: ").pack()
    Entry(log_screen, textvariable=username).pack()
    Label(log_screen, text="Password: ").pack()
    Entry(log_screen, textvariable=password, show="*").pack()
    Label(log_screen, text=" ").pack()
    Button(log_screen, text="Login", width=30, height=2, command=lambda: login(log_screen,username.get(), password.get())).pack()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Home Page")

    # create the menu bar
    menubar= Menu(screen)
    usermenu = Menu(menubar, tearoff=0)
    usermenu.add_command(label="Login", command=connect)
    usermenu.add_command(label="Sign Up", command=register)
    # usermenu.add_command(label="Save", command=pass)
    usermenu.add_separator()
    usermenu.add_command(label="Exit",command=lambda:screen.destroy())
    menubar.add_cascade(label="User", menu=usermenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...",command=lambda: webbrowser.open('https://github.com/Segev955/HackAu/blob/main/README.md'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    screen.config(menu=menubar)
    Label(text="Welcome to our hackton project!", bg="gray", width=300, height=1, font=("Calibri", 13)).pack()

    # Label(text=" ").pack()
    # Button(text="Login", width=30, height=2, command=connect).pack()
    # Label(text=" ").pack()
    # Button(text="Register", width=30, height=2, command=register).pack()

    screen.mainloop()


main_screen()
