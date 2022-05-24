import json

#
# class user_host:
#     def __init__(self, username: str, gender: str):
#         self.username = username
#         self.gender = gender
#         self.grade = 0
#         self.rates = 0
#         self.meals = []
#
#     def rate(self, grade: float):
#         self.rates += 1
#         self.grade += grade
#
#     def new_meal(self, meal: meal):
#         self.meals.append(meal)
#
#     def del_meal(self, meal: meal):
#         self.meals.remove(meal)
#

# class user_guest:
#     def __init__(self, username: str, gender: str):
#         self.username = username
#         self.gender = gender
#         self.requests = []
#         self.accepts = []
#
#     def request(self, mealid):
#         self.requests.append(mealid)
#
#     def accept(self, mealid):
#         if mealid not in self.requests:
#             return False
#         self.requests.remove(mealid)
#         self.accepts.append(mealid)
#         return True
#

class Meal:
    def __init__(self, host: str, title: str, date: tuple, time: tuple, address: str,capacity: int, guests= [], details=None, picture=None, kosher=None,id=-1):
        self.host = host
        self.title = title
        self.date = date
        self.time = time
        self.address = address
        self.capacity = capacity
        self.guests = guests
        self.details = details
        self.picture = picture
        self.kosher = kosher
        self.id=id
    def setId(self,id):
        self.id=id
    def strdate(self):
        return f"{self.date[0]}/{self.date[1]}/{self.date[2]}"
    def strtime(self):
        return f"{self.time[0]}:{self.time[1]}"
    def __repr__(self) -> str:
        return f"meal: {self.title} address: {self.address},date: {self.strdate()}, {self.strtime()}"

    #
    # def accept(self, guest: user_guest):
    #     if len(self.guests) >= self.capacity:
    #         return False
    #     self.guests.append(guest)
    #     return True

class Meals:
    def __init__(self):
        self.p = {}
    def load_from_json(self, file_name="meals.json"):
        with open(file_name) as f:
            dict = json.load(f)
            for id,meal in dict.items():
                self.p[meal[0]]=Meal(meal[1],meal[2],meal[3],meal[4],meal[5],meal[6],meal[7],meal[8],meal[9],meal[10],meal[0])
    def save_to_json(self,meal:Meal, file_name="meals.json"):
        with open(file_name) as f:
            j = json.load(f)
        j[meal.id]=(meal.id,meal.host, meal.title, meal.date, meal.time, meal.address,meal.capacity,meal.guests,meal.details,meal.picture,meal.kosher)
        with open(file_name, 'w') as jf:
            json.dump(j, jf, indent=4, separators=(',', ': '))
    def newmeal(self, meal: Meal):
        # if meal.host == "":
        #     return False, "Please input Host."
        if meal.title == "":
            return False, "Please input Title."
        if meal.date is None:
            return False, "Please choose Date."
        if meal.date[0] == -1:
            return False, "Please choose Year."
        if meal.date[1] == -1:
            return False, "Please choose Month."
        if meal.date[2] == -1:
            return False, "Please choose Day."
        if meal.time is None:
            return False, "Please choose time."
        if meal.time[0] == -1:
            return False, "Please choose Hour."
        if meal.time[1] == -1:
            return False, "Please choose Minuets."
        if meal.address =="":
            return False, "Please choose Address."
        meal.setId(len(self.p)+1)
        print(meal.id)
        self.p[meal.id]=meal
        self.save_to_json(meal)
        return True, f'{meal.title} meal added successfully!'

