import os
import sys
import time
import tkinter.messagebox
from threading import Thread
from tkinter import *
from tkinter import ttk
import datetime as dt
import webbrowser
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

from client import Client

CLIENT = Client()

def date_from_str(date: str, spliter='/') -> tuple:
    if date is None or len(date.split(spliter)) != 3: return None
    tup = (int(date.split(spliter)[1]), int(date.split(spliter)[0]), int(date.split(spliter)[2]))
    return tup


def date_from_strvars(day, month, year) -> tuple:
    d, m, y = (-1, -1, -1)
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
    return (d, m, y)


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


def chekcPass(username, password) -> tuple:
    if not CLIENT.send_message(f"CHECKPASS,{username},{password}"):
        return (False, "unalbe to connect the Server.")
    msg = CLIENT.get_messages()
    while len(msg) == 0 or msg[-1].split(',')[0] != 'CHECKPASS':
        msg = CLIENT.get_messages()
    return (msg[-1].split(',')[1] == 'True', msg[-1].split(',')[2])


def checkNewUser(username, password, gender, bdate, type) -> tuple:
    if not CLIENT.send_message(f"NEWUSER,{username},{password},{gender},{bdate},{type}"):
        return (False, "unalbe to connect the Server.")
    msg = CLIENT.get_messages()
    while len(msg) == 0 or msg[-1].split(',')[0] != 'NEWUSER':
        msg = CLIENT.get_messages()
    return (msg[-1].split(',')[1] == 'True', msg[-1].split(',')[2])


def checkType(name: str) -> str:
    CLIENT.send_message(f"CHECKTYPE,{name}")

    msg = CLIENT.get_messages()
    while len(msg) == 0 or msg[-1].split(',')[0] != 'TYPE':
        msg = CLIENT.get_messages()
    return msg[-1].split(',')[2]


def singup(username: str, password: str, gender: str, bdate: tuple, type: str):
    f, msg = checkNewUser(username, password, gender, f"{bdate[2]}.{bdate[1]}.{bdate[0]}", type)
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

def bg_photo(filename:str,size,screen):
    global img
    img = Image.open(filename)
    img_resized = img.resize(size)
    img = ImageTk.PhotoImage(img_resized)
    b2 = Label(screen, image=img)  # using Button
    b2.place(x=0, y=0)
def create_menu_bar(window):
    menubar = Menu(window)
    usermenu = Menu(menubar, tearoff=0)
    usermenu.add_command(label="Login", command=lambda: connect())
    usermenu.add_command(label="Sign Up", command=lambda: register())
    # usermenu.add_command(label="Dinner", command=lambda: dinner())
    usermenu.add_separator()
    usermenu.add_command(label="Exit", command=lambda: exit_win(window))
    menubar.add_cascade(label="User", menu=usermenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...",
                         command=lambda: webbrowser.open('https://github.com/Segev955/HackAu/blob/main/README.md'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)


def DatePicker(window, day, month, year, relx, rely, space, x):
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
        dayl.place(relx=relx + 2 * space, rely=rely)

    # Month:
    monthl = ttk.Combobox(window, textvariable=month, values=month_list)
    month.set("Month")
    monthl.config(width=7)
    monthl.place(relx=relx + space, rely=rely)
    monthl.bind('<<ComboboxSelected>>', select)
    elements.append(monthl)
    # Day:
    dayl = ttk.Combobox(window, textvariable=day)
    day.set("Day")
    dayl.config(width=5)
    dayl.place(relx=relx + 2 * space, rely=rely)
    elements.append(dayl)
    # Year:
    year_now = dt.date.today().year
    if x == 1:
        year_list = list(range(year_now - 100, year_now))
        year_list.reverse()
    else:
        year_list = list(range(year_now, year_now + 10))
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
    elements.append(DatePicker(WIN, day, month, year, 0.25, 0.65, 0.25, 1))
    elements.append(Radiobutton(WIN, text="Host", variable=typevar, value=0))
    elements[-1].place(relx=0.0, rely=0.8)
    elements.append(Radiobutton(WIN, text="Guest", variable=typevar, value=1))
    elements[-1].place(relx=0.15, rely=0.8)
    elements.append(Button(WIN, text="Sign Up", width=10, height=2,
                           command=lambda: singup(username=username.get(), password=password.get(),
                                                  gender=getGender(gender.get()),
                                                  bdate=date_from_strvars(day, month, year),
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
    elements.append(
        Button(WIN, text="Login", width=10, height=2, command=lambda: login(username.get(), password.get())))
    elements[-1].place(relx=0.45, rely=0.4)


def timePicker(window, minute, hour, relx, rely, space):
    min_list = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                '17',
                '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']
    hour_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                 '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '00']

    # Hour:
    hourl = ttk.Combobox(window, textvariable=hour, values=hour_list)
    hour.set("Hour")
    hourl.config(width=7)
    hourl.place(relx=relx + space, rely=rely)
    elements.append(hourl)
    # Minute:
    minl = ttk.Combobox(window, textvariable=minute, values=min_list)
    minute.set("Minute")
    minl.config(width=5)
    minl.place(relx=relx + 2 * space, rely=rely)
    elements.append(minl)


def dinner():
    def upload_file():
        global img
        f_types = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
        filename = tkinter.filedialog.askopenfilename(filetypes=f_types)
        img = Image.open(filename)
        img_resized = img.resize((50, 50))
        img = ImageTk.PhotoImage(img_resized)
        b2 = Label(WIN, image=img)  # using Button
        b2.place(relx=0.2, rely=0.40)

    destroy_elements(elements)
    WIN.title("Dinner")
    WIN.geometry("450x650")


    WIN.iconbitmap(os.path.join('icon', 'meal.ico'))
    create_menu_bar(WIN)
    # bg = Image.open("icon/bg.png")
    # bg_resized = bg.resize((450, 650))
    # bg = ImageTk.PhotoImage(bg_resized)
    #
    # print(bg)
    # l1 = Label(WIN, image=bg)
    # l1.place(x=0, y=0)
    # Var:
    bg_photo('icon/bg.png',(450,650), WIN)
    day = IntVar()
    month = IntVar()
    year = IntVar()
    minute = IntVar()
    hour = IntVar()
    address = StringVar()
    kosher = IntVar()
    details = StringVar()

    # Elements:
    elements.append(Label(WIN, text="Submit dinner", bg="gray", width=300, height=1,
                          font=("Calibri", 13)))
    elements[-1].pack()
    elements.append(Label(WIN, text="Title: "))
    elements[-1].place(relx=0.0, rely=0.05)
    elements.append(Entry(WIN, textvariable=address))
    elements[-1].place(relx=0.2, rely=0.05)
    elements.append(Label(WIN, text="Date: "))
    elements[-1].place(relx=0.0, rely=0.10)
    elements.append(DatePicker(WIN, day, month, year, 0.2, 0.1, 0.2, 0))
    elements.append(Label(WIN, text="Time: "))
    elements[-1].place(relx=0.0, rely=0.15)
    elements.append(timePicker(WIN, minute, hour, 0.2, 0.15, 0.2))
    elements.append(Label(WIN, text="Address: "))
    elements[-1].place(relx=0.0, rely=0.20)
    elements.append(Entry(WIN, textvariable=address))
    elements[-1].place(relx=0.2, rely=0.20)
    elements.append(Label(WIN, text="Capacity: "))
    elements[-1].place(relx=0.0, rely=0.25)
    elements.append(Spinbox(WIN, from_=1, to=100, width=3))
    elements[-1].place(relx=0.2, rely=0.25)
    elements.append(Label(WIN, text="Kosher: "))
    elements[-1].place(relx=0.0, rely=0.32)
    elements.append(Radiobutton(WIN, text="Kosher", variable=kosher, value=0))
    elements[-1].place(relx=0.1, rely=0.30)
    elements.append(Radiobutton(WIN, text="None", variable=kosher, value=1))
    elements[-1].place(relx=0.1, rely=0.35)
    elements.append(Radiobutton(WIN, text="Kosher rabanut", variable=kosher, value=2))
    elements[-1].place(relx=0.25, rely=0.30)
    elements.append(Radiobutton(WIN, text="Kosher mehadrin", variable=kosher, value=3))
    elements[-1].place(relx=0.25, rely=0.35)
    elements.append(Button(WIN, text="Upload image", command=lambda: upload_file()))
    elements[-1].place(relx=0.0, rely=0.43)
    elements.append(Label(WIN, text="Details: "))
    elements[-1].place(relx=0.0, rely=0.50)
    text = Text(WIN, height=8, width=45)
    elements.append(text)
    elements[-1].place(relx=0.15, rely=0.50)
    details = elements[-1].get("1.0", "end")
    elements.append(Button(WIN, text="Submit", width=10, height=2))
    elements[-1].place(relx=0.4, rely=0.80)


def open_user_win(username: str):
    try:
        CLIENT.send_message(f"RENAME,{CLIENT.name},{username}")
    except:
        return (False, "unalbe to connect the Server.")
    if checkType(username) == "HOST":
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
    elements.append(Button(text="create new meal",command=lambda: dinner()))
    elements[-1].pack()
    # CLIENT.send_message('USERTOSTRING')
    # msg = CLIENT.get_messages()
    # while len(msg) == 0 or msg[-1].split(',')[0] != 'USERTOSTRING':
    #     msg = CLIENT.get_messages()
    # Label(screen, text=msg[-1].split(',')[1]).pack()


elements = []


def destroy_elements(elements):
    for i in range(len(elements)):
        try:
            elements[i].destroy()
            # elements.pop(i)
        except:
            pass
    elements = []
    print(elements)


def isClientConnected(window, label, relx=0, rely=0, relwidth=0.1):
    while (True):
        if CLIENT.isconnected:
            l = Label(window, text="online", bg="green", width=350, height=1, font=("Calibri", 13)).place(relx=relx,
                                                                                                          rely=rely,
                                                                                                          relwidth=relwidth)
        else:
            l = Label(window, text="offline", bg="red", width=350, height=1, font=("Calibri", 13)).place(relx=relx,
                                                                                                         rely=rely,
                                                                                                         relwidth=relwidth)

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