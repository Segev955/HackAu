import tkinter.messagebox

import webbrowser
from tkinter import *
from tkinter import ttk

from tkcalendar import Calendar
import datetime as dt
from calendar import month_name

from users import *

u = Users()
day_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


def date_from_str(date: str, spliter='/') -> tuple:
    print(date)
    if date is None or len(date.split(spliter)) != 3: return None
    tup = (int(date.split(spliter)[1]), int(date.split(spliter)[0]), int(date.split(spliter)[2]))
    return tup


def getGender(g: int):
    if g == 0:
        return "male"
    elif g == 1:
        return "female"
    elif g == 2:
        return "other"
    # match (g):
    #     case 0:
    #         return "male"
    #     case 1:
    #         return "female"
    #     case 2:
    #         return "other"


def getType(t: int):
    if t == 0:
        return "Host"
    elif t == 1:
        return "Guest"
    # match (t):
    #     case 0:
    #         return "Host"
    #     case 1:
    #         return "Guest"


def singup(screen, username: str, password: str, gender: str, bdate: tuple, type: int):
    user = User(username=username, password=password, gender=gender, bdate=bdate, type=type)
    f, msg = u.newuser(user)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen, user)
    else:
        tkinter.messagebox.showerror(message=msg)


def login(screen, username, password):
    print(username)
    print(password)
    f, msg = u.chekcpass(username=username, password=password)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen,
                      User(username=username, password=password, gender=u.p[username][2], bdate=u.p[username][3],
                           type=u.p[username][4]))
    else:
        tkinter.messagebox.showerror(message=msg)


def open_user_win(window, user):
    window.destroy()
    if user.type == "Host":
        host_screen(user)
    else:
        guest_screen(user)


def create_menu_bar(window):
    menubar = Menu(window)
    # homemenu = Menu(menubar, tearoff=0)
    # homemenu.add_command(label="Home Page", command=lambda: homemenu())
    # menubar.add_cascade(label="Home", menu=homemenu)
    usermenu = Menu(menubar, tearoff=0)
    usermenu.add_command(label="Login", command=lambda: connect(window))
    usermenu.add_command(label="Sign Up", command=lambda: register(window))
    # usermenu.add_command(label="Save", command=pass)
    usermenu.add_separator()
    usermenu.add_command(label="Exit", command=lambda: window.destroy())
    menubar.add_cascade(label="User", menu=usermenu)
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...",
                         command=lambda: webbrowser.open('https://github.com/Segev955/HackAu/blob/main/README.md'))
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)


# def select(event):
#     print(monthl.get())
# if monthl.get() == month_list[1]:
#     print("feb")

def register(window=None):
    def select(event):
        if monthl.get() == '02':
            dayl = ttk.Combobox(reg_screen, textvariable=day, values=day_list[:28])
        elif monthl.get() == ('04' or '06' or '09' or '11'):
            dayl = ttk.Combobox(reg_screen, textvariable=day, values=day_list[:30])
        else:
            dayl = ttk.Combobox(reg_screen, textvariable=day, values=day_list)
        day.set("Day")
        dayl.config(width=15)
        dayl.place(relx=0.25, rely=0.41)

    reg_screen = Toplevel(home_screen)
    reg_screen.title("Register")
    reg_screen.geometry("300x500")
    if window is not None:
        window.destroy()
    create_menu_bar(reg_screen)

    username = StringVar()
    password = StringVar()
    gender = IntVar()
    type = IntVar()
    day = IntVar()
    month = IntVar()
    year = IntVar()
    Label(reg_screen, text="Register Form", font=(18)).place(relx=0.3, rely=0.01)
    Label(reg_screen, text="Username: ").place(relx=0, rely=0.1)
    Entry(reg_screen, textvariable=username).place(relx=0.25, rely=0.1)
    Label(reg_screen, text="Password: ").place(relx=0.0, rely=0.15)
    Entry(reg_screen, textvariable=password, show="*").place(relx=0.25, rely=0.15)
    Label(reg_screen, text="Gender: ").place(relx=0.0, rely=0.25)
    Radiobutton(reg_screen, text="male", variable=gender, value=0).place(relx=0.25, rely=0.2)
    Radiobutton(reg_screen, text="female", variable=gender, value=1).place(relx=0.25, rely=0.25)
    Radiobutton(reg_screen, text="other", variable=gender, value=2).place(relx=0.25, rely=0.3)
    Label(reg_screen, text="Date of birth: ").place(relx=0.0, rely=0.35)

    # Month:
    monthl = ttk.Combobox(reg_screen, textvariable=month, values=month_list)
    # monthl['values'] = [month_name[m][0:3] for m in range(1, 13)]
    # monthl['state'] = 'readonly'
    month.set("Month")
    monthl.config(width=15)
    monthl.place(relx=0.25, rely=0.35)
    monthl.bind('<<ComboboxSelected>>', select)
    # Day:
    dayl = ttk.Combobox(reg_screen, textvariable=day)
    day.set("Day")
    dayl.config(width=15)
    dayl.place(relx=0.25, rely=0.41)
    # Year:
    year_now = dt.date.today().year
    year_list = list(range(year_now - 100, year_now))
    yearl = ttk.Combobox(reg_screen, textvariable=year, values=year_list)
    year.set("Year")
    yearl.config(width=15)
    yearl.place(relx=0.25, rely=0.47)

    Radiobutton(reg_screen, text="Host", variable=type, value=0).place(relx=0.0, rely=0.6)
    Radiobutton(reg_screen, text="Guest", variable=type, value=1).place(relx=0.2, rely=0.6)
    Button(reg_screen, text="Sign Up", width=30, height=2,
           command=lambda: singup(screen=reg_screen, username=username.get(), password=password.get(),
                                  gender=getGender(gender.get()),
                                  bdate=(day.get(), month.get(), year.get()),
                                  type=getType(type.get())) in ()).place(relx=0.15, rely=0.7)


def connect(window=None):
    log_screen = Toplevel(home_screen)
    log_screen.title("Login")
    log_screen.geometry("300x250")
    if window is not None:
        window.destroy()
    create_menu_bar(log_screen)

    username = StringVar()
    password = StringVar()

    Label(log_screen, text="Please enter").pack()
    Label(log_screen, text=" ").pack()
    Label(log_screen, text="Username: ").pack()
    Entry(log_screen, textvariable=username).pack()
    Label(log_screen, text="Password: ").pack()
    Entry(log_screen, textvariable=password, show="*").pack()
    Label(log_screen, text=" ").pack()
    Button(log_screen, text="Login", width=30, height=2,
           command=lambda: login(log_screen, username.get(), password.get())).pack()


def guest_screen(user: User):
    screen = Toplevel(home_screen)
    screen.geometry("300x250")
    screen.title(f"Guest {user.username}")
    create_menu_bar(screen)


def host_screen(user: User):
    screen = Toplevel(home_screen)
    screen.geometry("300x250")
    screen.title(f"Host {user.username}")
    create_menu_bar(screen)


def home_page(window=None):
    global home_screen
    home_screen = Tk()
    home_screen.title("Home Page")
    home_screen.geometry("300x250")
    if window is not None:
        window.destroy()
    # create_menu_bar(home_screen)
    Label(home_screen, text="Welcome to our hackton project!", bg="gray", width=300, height=1,
          font=("Calibri", 13)).pack()

    Label(text=" ").pack()
    Button(text="Login", width=30, height=2, command=lambda: connect()).pack()
    Label(text=" ").pack()
    Button(text="Register", width=30, height=2, command=lambda: register()).pack()

    home_screen.mainloop()


home_page()
