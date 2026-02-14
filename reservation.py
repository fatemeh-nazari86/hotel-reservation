from datetime import datetime


class Reservation:
    def __init__(self, username, room_id, check_in, check_out, guests, total_cost, status="active"):
        
        self.username = username         
        self.room_id = room_id            
        self.check_in = check_in            
        self.check_out = check_out          
        self.guests = guests               
        self.total_cost = total_cost        
        self.status = status                # وضعیت رزرو (active / completed / cancelled)

    def to_dict(self):
        """
        تبدیل شیء رزرو به دیکشنری برای ذخیره در فایل JSON
        """
        return {
            "username": self.username,
            "room_id": self.room_id,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "guests": self.guests,
            "total_cost": self.total_cost,
            "status": self.status
        }


    # وقتی رزروها را از reservations.json می‌خوانیم می‌خواهیم دوباره شیء بسازیم
    @staticmethod
    def from_dict(data): 
        
        return Reservation(
            data["username"],
            data["room_id"],
            data["check_in"],
            data["check_out"],
            data["guests"],
            data["total_cost"],
            data["status"]
        )

    #بررسی اینکه آیا این رزرو تمام شده است یا نه
    def is_past(self):
        
        check_out_date = datetime.strptime(self.check_out, "%Y-%m-%d")
        return check_out_date < datetime.now()
