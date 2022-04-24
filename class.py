


class user_host:
    def __init__(self, username: str, gender: str):
        self.username = username
        self.gender = gender
        self.grade = 0
        self.rates = 0
        self.meals = []

    def rate(self, grade: float):
        self.rates += 1
        self.grade += grade

    def new_meal(self, meal: meal):
        self.meals.append(meal)

    def del_meal(self, meal: meal):
        self.meals.remove(meal)


class user_guest:
    def __init__(self, username: str, gender: str):
        self.username = username
        self.gender = gender
        self.requests = []
        self.accepts = []

    def request(self, mealid):
        self.requests.append(mealid)

    def accept(self, mealid):
        if mealid not in self.requests:
            return False
        self.requests.remove(mealid)
        self.accepts.append(mealid)
        return True


class meal:
    def __init__(self, id: int, title: str, date: tuple, time: tuple, address: str, price: float, host: user_host,
                 capacity: int,
                 guests: [], details=None, picture=None, kosher=None):
        self.id = id
        self.title = title
        self.date = date
        self.time = time
        self.address = address
        self.price = price
        self.host = host
        self.capacity = capacity
        self.guests = guests
        self.details = details
        self.picture = picture
        self.kosher = kosher

    def accept(self, guest: user_guest):
        if len(self.guests) >= self.capacity:
            return False
        self.guests.append(guest)
        return True
