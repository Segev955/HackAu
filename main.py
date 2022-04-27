import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import datetime as dt
import webbrowser


from users import *

u = Users()


def date_from_str(date: str, spliter='/') -> tuple:
    print(date)
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

def singup(screen, username: str, password: str, gender: str, bdate: tuple, type: str):
    user = User(username=username, password=password, gender=gender, bdate=bdate, type=type)
    f, msg = u.newuser(user)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen, user)
    else:
        tkinter.messagebox.showerror(message=msg)

def login(screen, username, password):
    f, msg = u.chekcpass(username=username, password=password)
    if f:
        tkinter.messagebox.showinfo(message=msg)
        open_user_win(screen,username)
    else:
        tkinter.messagebox.showerror(message=msg)

def create_menu_bar(window):
    menubar = Menu(window)
    usermenu = Menu(menubar, tearoff=0)
    usermenu.add_command(label="Login", command=lambda: connect(window))
    usermenu.add_command(label="Sign Up", command=lambda: register(window))
    usermenu.add_separator()
    usermenu.add_command(label="Exit", command=lambda: window.destroy())
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
        dayl.place(relx=0.75, rely=rely)
    # Month:
    monthl = ttk.Combobox(window, textvariable=month, values=month_list)
    month.set("Month")
    monthl.config(width=7)
    monthl.place(relx=relx+space, rely=rely)
    monthl.bind('<<ComboboxSelected>>', select)
    # Day:
    dayl = ttk.Combobox(window, textvariable=day)
    day.set("Day")
    dayl.config(width=5)
    dayl.place(relx=relx+2*space, rely=rely)
    # Year:
    year_now = dt.date.today().year
    year_list = list(range(year_now - 100, year_now))
    year_list.reverse()
    yearl = ttk.Combobox(window, textvariable=year, values=year_list)
    year.set("Year")
    yearl.config(width=7)
    yearl.place(relx=relx, rely=rely)
    yearl.bind('<<ComboboxSelected>>', select)

def register(window=None):
    reg_screen = Toplevel(home_screen)
    reg_screen.title("Register")
    reg_screen.geometry("300x250")
    reg_screen.iconbitmap(os.path.join('icon', 'register.ico'))
    if window is not None:
        window.destroy()
    create_menu_bar(reg_screen)

    username = StringVar()
    password = StringVar()
    gender = IntVar()
    typevar = IntVar()
    day = IntVar()
    month = IntVar()
    year = IntVar()


    Label(reg_screen, text="Register Form", font=(18)).place(relx=0.3, rely=0.05)
    Label(reg_screen, text="Username: ").place(relx=0, rely=0.2)
    Entry(reg_screen, textvariable=username).place(relx=0.25, rely=0.2)
    Label(reg_screen, text="Password: ").place(relx=0.0, rely=0.3)
    Entry(reg_screen, textvariable=password, show="*").place(relx=0.25, rely=0.3)
    Label(reg_screen, text="Gender: ").place(relx=0.0, rely=0.45)
    Radiobutton(reg_screen, text="male", variable=gender, value=0).place(relx=0.25, rely=0.4)
    Radiobutton(reg_screen, text="female", variable=gender, value=1).place(relx=0.25, rely=0.5)
    Radiobutton(reg_screen, text="other", variable=gender, value=2).place(relx=0.5, rely=0.45)

    Label(reg_screen, text="Date of birth: ").place(relx=0.0, rely=0.65)
    DatePicker(reg_screen, day, month, year)

    Radiobutton(reg_screen, text="Host", variable=typevar, value=0).place(relx=0.0, rely=0.8)
    Radiobutton(reg_screen, text="Guest", variable=typevar, value=1).place(relx=0.2, rely=0.8)

    Button(reg_screen, text="Sign Up", width=10, height=2,
           command=lambda: singup(screen=reg_screen, username=username.get(), password=password.get(),
                   gender=getGender(gender.get()),
                   bdate=date_from_strvars(day,month,year),
                   type=getType(typevar.get())) in ()).place(relx=0.4, rely=0.75)

def connect(window=None):
    log_screen = Toplevel(home_screen)
    log_screen.title("Login")
    log_screen.geometry("300x250")
    log_screen.iconbitmap(os.path.join('icon', 'login.ico'))
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

def open_user_win(window, username):
    window.destroy()
    if u.p[username].type == "Host":
        host_screen(u.p[username])
    else:
        guest_screen(u.p[username])

def guest_screen(user: User):
    screen = Toplevel(home_screen)
    screen.geometry("300x250")
    screen.title(f"Guest {user.username}")
    create_menu_bar(screen)
    Label(screen, text=user).pack()

def host_screen(user: User):
    screen = Toplevel(home_screen)
    screen.geometry("300x250")
    screen.title(f"Host {user.username}")
    create_menu_bar(screen)
    Label(screen, text=user).pack()




def home_page(window=None):
    global home_screen
    home_screen = Tk()
    home_screen.title("Home Page")
    home_screen.geometry("300x250")
    home_screen.iconbitmap(os.path.join('icon', 'meal.ico'))
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
