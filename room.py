from datetime import datetime, timedelta

class Room:
    # کلاس پایه که بقیه کلاس‌ها ازش ارث‌بردی می‌کنند
    def __init__(self, room_id, room_type, price_per_night, amenities, capacity):
        self.room_id = room_id                        # شماره اتاق
        self.room_type = room_type
        self._price_per_night = price_per_night       # قیمت هر شب 
        self.amenities = amenities                    # امکانات اتاق
        self.capacity = capacity                      # ظرفیت نفرات
        self.is_reserved = False                      # آیا اتاق رزرو شده یا نه

    # محاسبه قیمت 
    def calculate_price(self, check_in, check_out):
        nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
        total=nights * self._price_per_night
        return 'bedon takhfif:', int(total)

    def to_dict(self):
        # تبدیل شیء به دیکشنری برای ذخیره در فایل JSON
        return {
            "room_id": self.room_id,
            "price_per_night": self._price_per_night,
            "amenities": self.amenities,
            "capacity": self.capacity,
            "is_reserved": self.is_reserved
        }


class StandardRoom(Room):
   
    def calculate_price(self, check_in, check_out):

        nights = (datetime.strptime(check_out, "%Y-%m-%d") -datetime.strptime(check_in, "%Y-%m-%d")).days

        total = nights * self._price_per_night
        discount_msg = 'bedon takhfif:'

        # تخفیف رزرو بلندمدت (بیشتر از 7 شب)
        if nights > 7:
            total *= 0.9   # 10٪ تخفیف
            discount_msg = "ba ٪10 takhfif rezerv boland modat:"
            
        return discount_msg ,int(total)


class SuiteRoom(Room):
    
    def calculate_price(self, check_in, check_out):
        
        nights = (datetime.strptime(check_out, "%Y-%m-%d") -datetime.strptime(check_in, "%Y-%m-%d")).days

        total = nights * self._price_per_night
        service_fee = 200000
        total += service_fee
        discount_msg = f"hazine khadamat {service_fee}"

        # تخفیف رزرو زودهنگام (14 روز قبل)
        if (datetime.strptime(check_in, "%Y-%m-%d") - datetime.now()) >= timedelta(days=14):
            total *= 0.85   # 15٪ تخفیف
            discount_msg += "va 15٪ takhfif rezerv zood hengam: "
        
        return  discount_msg,int(total)
    


