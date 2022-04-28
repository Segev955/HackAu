import os
import sys
import time
import tkinter.messagebox
from threading import Thread
from tkinter import *
from tkinter import ttk
import datetime as dt
import webbrowser
from client import Client

CLIENT=Client()



def date_from_str(date: str, spliter='/') -> tuple:
    if date is None or len(date.split(spliter)) != 3: return None
    tup = (int(date.split(spliter)[1]), int(date.split(spliter)[0]), int(date.split(spliter)[2]))
    return tup

def date_from_strvars(day,month,year) -> tuple:
    d,m,y=(-1,-1,-1)
    try:
        d = day.get()
    except:
        pass
    try:
        m = month.get()
    except:
        pass
    try:
        y = year.get()
    except:
        pass
    return (d,m,y)

def getGender(g: int):
    if g == 0:
        return "male"
    elif g == 1:
        return "female"
    else:
        return "other"

def getType(t: int):
    if t == 0:
        return "Host"
    else:
        return "Guest"

def chekcPass(username, password)->tuple:
    if not CLIENT.send_message(f"CHECKPASS,{username},{password}"):
        return (False, "unalbe to connect the Server.")
    msg = CLIENT.get_messages()
    while len(msg)==0 or msg[-1].split(',')[0] != 'CHECKPASS':
        msg = CLIENT.get_messages()
    return (msg[-1].split(',')[1]=='True',msg[-1].split(',')[2])

def checkNewUser(username, password, gender, bdate, type)->tuple:
    if not CLIENT.send_message(f"NEWUSER,{username},{password},{gender},{bdate},{type}"):
        return (False, "unalbe to connect the Server.")
    msg = CLIENT.get_messages()
    while len(msg)==0 or msg[-1].split(',')[0] != 'NEWUSER':
        msg = CLIENT.get_messages()
    return (msg[-1].split(',')[1]=='True',msg[-1].split(',')[2])

def checkType(name:str)->str:
    if not CLIENT.send_message(f"CHECKTYPE,{name}"):
        return "unalbe to connect the Server."
    msg = CLIENT.get_messages()
    while len(msg) == 0 or msg[-1].split(',')[0] != 'TYPE':
        msg = CLIENT.get_messages()
    return msg[-1].split(',')[2]

def singup(username: str, password: str, gender: str, bdate: tuple, type: str):
    f, msg = checkNewUser(username,password,gender,f"{bdate[2]}.{bdate[1]}.{bdate[0]}",type)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(username)
    else:
        tkinter.messagebox.showerror(message=msg)

def login(username, password):
    f, msg = chekcPass(username=username, password=password)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(username)
    else:
        tkinter.messagebox.showerror(message=msg)

def exit_win(window):
    CLIENT.disconnect()
    window.destroy()
    sys.exit()

def create_menu_bar(window):
    menubar = Menu(window)
    usermenu = Menu(menubar, tearoff=0)
    usermenu.add_command(label="Login", command=lambda: connect())
    usermenu.add_command(label="Sign Up", command=lambda: register())
    usermenu.add_separator()
    usermenu.add_command(label="Exit", command=lambda: exit_win(window))
    menubar.add_cascade(label="User", menu=usermenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...",command=lambda: webbrowser.open('https://github.com/Segev955/HackAu/blob/main/README.md'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)

def DatePicker(window,day,month,year,relx=0.25, rely=0.65,space=0.25):
    day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    def select(event):
        if monthl.get() == '02':
            if yearl.get() != 'Year' and int(yearl.get()) % 4 == 0:
                dayl = ttk.Combobox(window, textvariable=day, values=day_list[:29])
            else:
                dayl = ttk.Combobox(window, textvariable=day, values=day_list[:28])
        elif monthl.get() == ('04' or '06' or '09' or '11'):
            dayl = ttk.Combobox(window, textvariable=day, values=day_list[:30])
        else:
            dayl = ttk.Combobox(window, textvariable=day, values=day_list)
        day.set("Day")
        dayl.config(width=5)
        dayl.place(relx=relx+2*space, rely=rely)
    # Month:
    monthl = ttk.Combobox(window, textvariable=month, values=month_list)
    month.set("Month")
    monthl.config(width=7)
    monthl.place(relx=relx+space, rely=rely)
    monthl.bind('<<ComboboxSelected>>', select)
    elements.append(monthl)
    # Day:
    dayl = ttk.Combobox(window, textvariable=day)
    day.set("Day")
    dayl.config(width=5)
    dayl.place(relx=relx+2*space, rely=rely)
    elements.append(dayl)
    # Year:
    year_now = dt.date.today().year
    year_list = list(range(year_now - 100, year_now))
    year_list.reverse()
    yearl = ttk.Combobox(window, textvariable=year, values=year_list)
    year.set("Year")
    yearl.config(width=7)
    yearl.place(relx=relx, rely=rely)
    yearl.bind('<<ComboboxSelected>>', select)
    elements.append(yearl)

def register():
    destroy_elements(elements)
    WIN.title("Register")
    WIN.geometry("450x250")
    WIN.iconbitmap(os.path.join('icon', 'register.ico'))
    create_menu_bar(WIN)

    username = StringVar()
    password = StringVar()
    gender = IntVar()
    typevar = IntVar()
    day = IntVar()
    month = IntVar()
    year = IntVar()

    elements.append(Label(WIN, text="Register Form", bg="gray", width=300, height=1, font=("Calibri", 13)))
    elements[-1].pack()
    elements.append(Label(WIN, text="Username: "))
    elements[-1].place(relx=0, rely=0.2)
    elements.append(Entry(WIN, textvariable=username))
    elements[-1].place(relx=0.17, rely=0.2)
    elements.append(Label(WIN, text="Password: "))
    elements[-1].place(relx=0.0, rely=0.3)
    elements.append(Entry(WIN, textvariable=password, show="*"))
    elements[-1].place(relx=0.17, rely=0.3)
    elements.append(Label(WIN, text="Gender: "))
    elements[-1].place(relx=0.0, rely=0.45)
    elements.append(Radiobutton(WIN, text="male", variable=gender, value=0))
    elements[-1].place(relx=0.1, rely=0.4)
    elements.append(Radiobutton(WIN, text="female", variable=gender, value=1))
    elements[-1].place(relx=0.1, rely=0.5)
    elements.append(Radiobutton(WIN, text="other", variable=gender, value=2))
    elements[-1].place(relx=0.25, rely=0.45)
    elements.append(Label(WIN, text="Date of birth: "))
    elements[-1].place(relx=0.0, rely=0.65)
    elements.append(DatePicker(WIN, day, month, year, relx=0.17, space=0.15))
    elements.append(Radiobutton(WIN, text="Host", variable=typevar, value=0))
    elements[-1].place(relx=0.0, rely=0.8)
    elements.append(Radiobutton(WIN, text="Guest", variable=typevar, value=1))
    elements[-1].place(relx=0.15, rely=0.8)
    elements.append(Button(WIN, text="Sign Up", width=10, height=2,
                           command=lambda: singup(username=username.get(), password=password.get(),
                                                      gender=getGender(gender.get()),
                                                      bdate=date_from_strvars(day,month,year),
                                                      type=getType(typevar.get())) in ()))
    elements[-1].place(relx=0.3, rely=0.75)

def connect():
    destroy_elements(elements)
    WIN.title("Login")
    WIN.geometry("450x130")
    WIN.iconbitmap(os.path.join('icon', 'login.ico'))
    create_menu_bar(WIN)

    username = StringVar()
    password = StringVar()

    elements.append(Label(WIN, text="Log in Form", bg="gray", width=300, height=1,
                          font=("Calibri", 13)))
    elements[-1].pack()
    elements.append(Label(WIN, text="Username: "))
    elements[-1].place(relx=0, rely=0.4)
    elements.append(Entry(WIN, textvariable=username))
    elements[-1].place(relx=0.15, rely=0.4)
    elements.append(Label(WIN, text="Password: "))
    elements[-1].place(relx=0.0, rely=0.6)
    elements.append(Entry(WIN, textvariable=password, show="*"))
    elements[-1].place(relx=0.15, rely=0.6)
    elements.append(Button(WIN, text="Login", width=10, height=2, command=lambda: login(username.get(), password.get())))
    elements[-1].place(relx=0.45, rely=0.4)

def open_user_win(username:str):
    try:
        CLIENT.send_message(f"RENAME,{CLIENT.name},{username}")
    except:
        return (False, "unalbe to connect the Server.")
    if checkType(username) == "Host":
        host_screen()
    else:
        guest_screen()
    return (True, f"Welcome to {username} window.")

def guest_screen():
    destroy_elements(elements)
    WIN.geometry("450x250")
    WIN.title(f"Guest {CLIENT.name}")
    create_menu_bar(WIN)
    elements.append(Label(WIN, text=f"Welcome {CLIENT.name}", bg="gray", width=300, height=1, font=("Calibri", 13)))
    elements[-1].pack()
    # CLIENT.send_message('USERTOSTRING')
    # msg = CLIENT.get_messages()
    # while len(msg) == 0 or msg[-1].split(',')[0] != 'USERTOSTRING':
    #     msg = CLIENT.get_messages()
    # Label(screen, text=msg[-1].split(',')[1]).pack()

def host_screen():
    destroy_elements(elements)
    WIN.geometry("450x250")
    WIN.title(f"Host {CLIENT.name}")
    create_menu_bar(WIN)
    elements.append(Label(WIN, text=f"Welcome {CLIENT.name}", bg="gray", width=300, height=1, font=("Calibri", 13)))
    elements[-1].pack()
    # CLIENT.send_message('USERTOSTRING')
    # msg = CLIENT.get_messages()
    # while len(msg) == 0 or msg[-1].split(',')[0] != 'USERTOSTRING':
    #     msg = CLIENT.get_messages()
    # Label(screen, text=msg[-1].split(',')[1]).pack()

elements=[]
def destroy_elements(elements):
    for i in range(len(elements)):
        try:
            elements[i].destroy()
            # elements.pop(i)
        except:
            pass
    elements=[]
    print(elements)

def isClientConnected(window,label,relx=0, rely=0, relwidth=0.1):
    while (True):
        if CLIENT.isconnected:
            l=Label(window, text="online", bg="green", width=350, height=1,font=("Calibri", 13)).place(relx=relx, rely=rely, relwidth=relwidth)
        else:
            l=Label(window, text="offline", bg="red", width=350, height=1,font=("Calibri", 13)).place(relx=relx, rely=rely, relwidth=relwidth)

        time.sleep(2)


def home_page(window=None):
    global WIN
    WIN = Tk()
    WIN.title("Home Page")
    WIN.geometry("450x250")
    WIN.iconbitmap(os.path.join('icon', 'meal.ico'))
    if window is not None:
        window.destroy()
    elements.append(Label(WIN, text="Welcome to our hackton project!", bg="gray", width=300, height=1,
                          font=("Calibri", 13)))
    elements[-1].pack()
    l = Label()
    con_thread = Thread(target=lambda: isClientConnected(window=WIN, label=l))
    con_thread.start()
    elements.append(l)
    elements[-1].pack()
    elements.append(Button(text="Login", width=30, height=2, command=lambda: connect()))
    elements[-1].pack()
    elements.append(Button(text="Register", width=30, height=2, command=lambda: register()))
    elements[-1].pack()



    WIN.mainloop()
home_page()

