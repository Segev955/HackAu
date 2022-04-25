import datetime
import json


class User:
    def __init__(self, username: str, password: str, gender: str, bdate: list, type: str):
        self.username = username
        self.password = password
        self.gender = gender
        self.bdate = bdate
        self.type = type


class Users:
    def __init__(self):
        self.p = {}

    def newuser(self, user: User):
        self.load_from_json()
        if user.username=="":
            return False, "Please Input Username."
        if user.password=="":
            return False, "Please Input Password."
        if user.gender is None:
            return False, "Please Choose Gender."
        if user.bdate is None:
            return False, "Please Choose Birth Date."
        if user.type is None:
            return False, "Please Choose Your Type."
        if user.username in self.p.keys():
            return False, "Username Exists."
        if len(user.password) < 5:
            return False, "Password Too Short."
        if len(user.username) < 5:
            return False, "Username Too Short."
        for c in user.username:
            if not c.isalpha() and not c.isnumeric() and not c in "_-.":
                return False, "Illegal Username."
        for c in user.password:
            if not c.isalpha() and not c.isnumeric() and not c in "_-.":
                return False, "Illegal Password."
        # t= int (datetime.date.today().year)
        # d,m,y=user.bdate
        # print(t-y)
        # if t-y<16:
        #     return False,"You Are Under Age 16"
        # if t-y>120:
        #     return False,"Birth Dath Not Sense."

        self.p[user.username] = user
        self.save_to_json(user)
        self.load_from_json()
        return True, f'Welcome {user.username}!'

    def chekcpass(self, username: str, password: str):
        print(username)
        self.load_from_json()
        print(self.p)
        if username=="":
            return False, "Please Input Username."
        if password=="":
            return False, "Please Input Password."
        if username not in self.p.keys():
            return False, "Username not exist!"
        if self.p[username][1] != password:
            return False, "Wrong password!"
        return True, f'Welcome {username}!'

    def deluser(self, username: str, password: str):
        if self.chekcpass(username, password):
            self.p.pop(username)
            return True
        return False

    def save_to_json(self, user:User, file_name="users.json"):
        j = {}
        with open(file_name) as f:
            j = json.load(f)
        j[user.username] = (user.username,user.password,user.gender, user.bdate, user.type)
        with open(file_name, 'w') as jf:
            json.dump(j, jf, indent=4, separators=(',', ': '))

    def load_from_json(self, file_name="users.json"):
        with open(file_name) as f:
            self.p = json.load(f)
