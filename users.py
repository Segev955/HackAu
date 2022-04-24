import json


class user:
    def __init__(self, username: str, password: str, gender: str, bdate: str, type: int):
        self.username = username
        self.password = password
        self.gender = gender
        self.bdate = bdate
        self.type = type


class users:
    def __init__(self):
        self.p = {}

    def newuser(self, user: user):
        if user.username in self.p.keys():
            return False, "Username exists"
        if len(user.password) < 5:
            return False, "password too short."
        if len(user.username) < 5:
            return False, "username too short."
        for c in user.username:
            if not c.isalpha() and not c.isnumeric() and not c in "_-.":
                return False, "illegal username."
        for c in user.password:
            if not c.isalpha() and not c.isnumeric() and not c in "_-.":
                return False, "illegal password."
        self.p[user.username] = user
        self.save_to_json(user)
        self.load_from_json()
        return True, f'Welcome {user.username}!'

    def chekcpass(self, username: str, password: str):
        if username not in self.p.keys():
            return False, "Username not exist!"
        if self.p[username] != password:
            return False, "Wrong password!"
        return True, f'Welcome {username}!'

    def deluser(self, username: str, password: str):
        if self.chekcpass(username, password):
            self.p.pop(username)
            return True
        return False

    def save_to_json(self, user:user, file_name="users.json"):
        j = {}
        with open(file_name) as f:
            j = json.load(f)
        j[user.username] = (user.username,user.password,user.gender, user.bdate, user.type)
        with open(file_name, 'w') as jf:
            json.dump(j, jf, indent=4, separators=(',', ': '))

    def load_from_json(self, file_name="users.json"):
        with open(file_name) as f:
            self.p = json.load(f)
