import datetime
import json


class User:
    def __init__(self, username: str, password: str, gender: str, bdate: list, type: str):
        self.username = username
        self.password = password
        self.gender = gender
        self.bdate = (bdate[2], bdate[1], bdate[0])
        self.type = type

    def getPass(self):
        return self.password

    def __repr__(self):
        return f"password: {self.password}, Birth Date: {self.bdate[0]}/{self.bdate[1]}/{self.bdate[2]}, User Type: {self.type}."

    def __str__(self):
        return f"{self.type} User {self.username}:\nBirth Date: {self.bdate[0]}/{self.bdate[1]}/{self.bdate[2]}\ngender: {self.gender}\n"


class Users:
    def __init__(self):
        self.p = {}

    def newuser(self, user: User):
        self.load_from_json()
        if user.username == "":
            return False, "Please input Username."
        if user.password == "":
            return False, "Please input Password."
        if user.gender is None:
            return False, "Please choose Gender."
        if user.bdate is None:
            return False, "Please choose Birth Date."
        if user.bdate[0] == -1:
            return False, "Please choose Year."
        if user.bdate[1] == -1:
            return False, "Please choose Month."
        if user.bdate[2] == -1:
            return False, "Please choose Day."
        if user.type is None:
            return False, "Please choose Your Type."
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

        self.p[user.username] = user
        self.save_to_json(user)
        self.load_from_json()
        return True, f'Welcome {user.username}!'

    def chekcpass(self, username: str, password: str):
        self.load_from_json()
        if username == "":
            return False, "Please Input Username."
        if password == "":
            return False, "Please Input Password."
        if username not in self.p.keys():
            return False, "Username not exist!"
        if self.p[username].getPass() != password:
            return False, "Wrong password!"
        return True, f'Welcome {username}!'

    def deluser(self, username: str, password: str):
        if self.chekcpass(username, password):
            self.p.pop(username)
            return True
        return False

    def save_to_json(self, user: User, file_name="users.json"):
        with open(file_name) as f:
            j = json.load(f)
        j[user.username] = (user.username, user.password, user.gender, user.bdate, user.type)
        with open(file_name, 'w') as jf:
            json.dump(j, jf, indent=4, separators=(',', ': '))

    def load_from_json(self, file_name="users.json"):
        with open(file_name) as f:
            dict = json.load(f)
            for name, user in dict.items():
                self.p[name] = User(user[0], user[1], user[2], user[3], user[4])
