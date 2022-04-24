import tkinter.messagebox
from tkinter import *

import users

u = users.users()
u.load_from_json()


def singup(username: str, password: str, gender: str, bdate: str, type: int):
    user = users.user(username=username, password=password, gender=gender, bdate=bdate, type=type)
    print("pass:")
    print(user.password)

    f, msg = u.newuser(user)
    if f:
        tkinter.messagebox.showinfo(message=msg)
    else:
        tkinter.messagebox.showerror(message=msg)


def login2(username, password):
    u.load_from_json()
    f, msg = u.chekcpass(username=username, password=password)
    if f:
        tkinter.messagebox.showinfo(message=msg)
    else:
        tkinter.messagebox.showerror(message=msg)


def register():
    reg_screen = Toplevel(screen)
    reg_screen.title("Register")
    reg_screen.geometry("300x400")

    username = StringVar()
    password = StringVar()
    gender = StringVar()
    bdate = StringVar()
    type = IntVar()

    Label(reg_screen, text="Please enter").pack()
    Label(reg_screen, text=" ").pack()
    Label(reg_screen, text="Username: ").pack()
    Entry(reg_screen, textvariable=username).pack()
    Label(reg_screen, text="Password: ").pack()
    Entry(reg_screen, textvariable=password, show="*").pack()
    Label(reg_screen, text="Gender: ").pack()
    Entry(reg_screen, textvariable=gender).pack()
    Label(reg_screen, text="Date of birth: ").pack()
    Entry(reg_screen, textvariable=bdate).pack()
    Radiobutton(reg_screen, text="Host", variable=type, value=1).pack()
    Radiobutton(reg_screen, text="Guest", variable=type, value=2).pack()
    Label(reg_screen, text=" ").pack()


    Button(reg_screen, text="Register", width=30, height=2,
           command=lambda: singup(username.get(),password.get(),gender.get(),bdate.get(),type.get()) in ()).pack()


def login():
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
    Button(log_screen, text="Login", width=30, height=2, command=lambda: login2(username.get(), password.get())).pack()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Host")
    Label(text="Login or Register", bg="gray", width=300, height=2, font=("Calibri", 13)).pack()
    Label(text=" ").pack()
    Button(text="Login", width=30, height=2, command=login).pack()
    Label(text=" ").pack()
    Button(text="Register", width=30, height=2, command=register).pack()

    screen.mainloop()


main_screen()
