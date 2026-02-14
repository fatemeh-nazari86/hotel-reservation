class User:
    def __init__(self, first_name, last_name, username, password, balance=0):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.balance = balance

    # افزایش اعتبار کاربر
    def add_balance(self, amount):
        self.balance =self.balance + amount

    # بررسی کافی بودن اعتبار
    def has_enough_balance(self, amount):
        return self.balance >= amount

 # کسر مبلغ از اعتبار کاربر در صورت کافی بودن    
    def pay(self, amount):
        if self.has_enough_balance(amount):
            self.balance -= amount
            return True
        return False

    # تبدیل شیء به دیکشنری برای ذخیره در فایل
    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "balance": self.balance
        }


    # ساخت شیء User از روی دیکشنری (JSON)
    @staticmethod
    def from_dict(data):
        return User(
            data["first_name"],
            data["last_name"],
            data["username"],
            data["password"],
            data["balance"]
        )
