import json
import os
from datetime import datetime ,timedelta
from room_manager import load_rooms
from reservation import Reservation
from room import Room, StandardRoom, SuiteRoom
from user_manager import update_user
from invoice_manager import create_invoice


# خواندن رزروها از فایل
def load_reservations():
    try:
        with open("reservations.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # اگر فایل وجود نداشت، لیست خالی برمی‌گرداند
        return []


# ذخیره رزروها در فایل
def save_reservations(reservations):
    with open("reservations.json", "w") as file:
        json.dump(reservations, file, indent=4)


# به‌روزرسانی خودکار وضعیت رزروها 
def update_reservations_status():
    reservations = load_reservations()
    now = datetime.now()
    changed = False

    for r in reservations:
        if r["status"] == "active":
            check_out = datetime.strptime(r["check_out"], "%Y-%m-%d")
            if check_out < now:
                r["status"] = "completed"
                changed = True

    if changed:
        save_reservations(reservations)

# نمایش رزروهای کاربر (همه یا فیلتر شده)
def show_user_reservations(user, status_filter=None):
    update_reservations_status()

    reservations = load_reservations()
    found = False

    print("\n--- list rezerv haye shoma ---")

    for r in reservations:
        if r["username"] == user.username:
            if status_filter is None or r["status"] == status_filter:
                found = True
                print(
                    f"otagh: {r['room_id']} | "
                    f"az {r['check_in']} ta {r['check_out']} | "
                    f"gheymat: {r['total_cost']} | "
                    f"vaziat: {r['status']}"
                )

    if not found:
        print("hich rezervi peyda nashod")

    input("baraye edame ENTER bezanid")


# لغو رزرو

def cancel_reservation(user):

    update_reservations_status()

    reservations = load_reservations()
    active_reservations = []

    # پیدا کردن رزروهای فعال کاربر
    for r in reservations:
        if r["username"] == user.username and r["status"] == "active":
            active_reservations.append(r)

    # اگر رزرو فعالی نداشت
    if len(active_reservations) == 0:
        print("hich rezerv faali nadarid")
        input("baraye edame ENTER bezanid")
        return

    # نمایش رزروهای فعال
    print("\n--- rezerv haye faal shoma ---")

    count = 1
    for r in active_reservations:
        print(
            f"{count}. otagh {r['room_id']} | "
            f"az {r['check_in']} ta {r['check_out']} | "
            f"gheymat {r['total_cost']}"
        )
        count += 1

    # انتخاب رزرو
    choice = int(input("shomare rezerv baraye laghv: "))

    # بررسی معتبر بودن انتخاب
    if choice < 1 or choice > len(active_reservations):
        print("entekhab eshtebah ast")
        input("baraye edame ENTER bezanid")
        return

    # رزرو انتخاب شده
    selected_reservation = active_reservations[choice - 1]

    # تبدیل تاریخ ورود به datetime
    check_in_date = datetime.strptime(
        selected_reservation["check_in"], "%Y-%m-%d"
    )

    now = datetime.now()

    # محاسبه مبلغ بازگشتی
    if check_in_date - now > timedelta(hours=48):
        refund = selected_reservation["total_cost"]
    else:
        refund = selected_reservation["total_cost"] * 0.5

    # بازگرداندن پول به کاربر
    user.balance += refund
    update_user(user)

    # تغییر وضعیت رزرو به cancelled
    for r in reservations:
        if r == selected_reservation:
            r["status"] = "cancelled"
            break

    save_reservations(reservations)

    print("rezerv ba movafaghiyat laghv shod")
    print(f"mablagh bargashti: {refund}")
    print(f"etebar jadid shoma: {user.balance}")
    input("baraye edame ENTER bezanid")



# بررسی تداخل تاریخ‌ها 
def is_date_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1


#  جستجوی اتاق‌های آزاد
def search_available_rooms(check_in, check_out):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

    # محاسبه تعداد شب‌ها
    nights = (check_out_date - check_in_date).days
    if nights <= 0:
        print("tarikh haye vared shode eshtebah ast")
        return []

    rooms = load_rooms()
    reservations = load_reservations()
    available_rooms = []

    for room in rooms:
        reserved = False

        # بررسی اینکه آیا این اتاق قبلاً رزرو شده یا نه
        for res in reservations:
            if res["room_id"] == room["room_id"]:
                res_start = datetime.strptime(res["check_in"], "%Y-%m-%d")
                res_end = datetime.strptime(res["check_out"], "%Y-%m-%d")

                if is_date_overlap(check_in_date, check_out_date, res_start, res_end):
                    reserved = True
                    break

        if not reserved:
    # اتاق آزاد را به کلاس مناسب تبدیل کنیم
            
            if room['room_type'] in ['1 takhte', '2 takhte']:
                room_obj = StandardRoom(
                    room['room_id'], room['room_type'], room['price_per_night'],
                    room['amenities'], room['capacity']
                )
            elif room['room_type'] == 'Suite':
                room_obj = SuiteRoom(
                    room['room_id'], room['room_type'], room['price_per_night'],
                    room['amenities'], room['capacity']
                )
            else:
                room_obj = Room(
                    room['room_id'], room['room_type'], room['price_per_night'],
                    room['amenities'], room['capacity']
                )

            #  محاسبه قیمت
            total_price = room_obj.calculate_price(check_in, check_out)

            room["total_price"] = total_price
            available_rooms.append(room)

    return available_rooms



#  ثبت رزرو واقعی
def create_reservation(user):
    while True:    
        print("=== sabt rezerv otagh ===")

        # دریافت تاریخ ورود و خروج
        check_in = input("tarikh vorood (YYYY-MM-DD): ")
        check_out = input("tarikh khorooj (YYYY-MM-DD): ")

        try:
            # گرفتن لیست اتاق‌های آزاد
            available_rooms = search_available_rooms(check_in, check_out)

            if not available_rooms:
                print("hich otagh azadi vojood nadarad")
                input("baraye edame ENTER bezanid")
                return

            # نمایش اتاق‌های قابل رزرو
            print("\n--- otagh haye ghabel rezerv---")
            for room in available_rooms:
                print(
                    f"otagh: {room['room_id']} | "
                    f"zarfiyat: {room['capacity']} | "
                    f"ghaymat kol: {room['total_price']}"
                )
            break
        except ValueError:
            print('lotfan tarikh ha ra dorost vared konid')
            input("baraye edame ENTER bezanid")
            os.system("cls")
            continue
        

    # انتخاب اتاق
    room_id = input("\nshomare otagh mored nazar: ")
    guests = int(input("tedad nafarat: "))

    selected_room = None
    for room in available_rooms:
        if str(room["room_id"]) == room_id:
            selected_room = room
            break

    # اگر اتاق انتخاب‌شده وجود نداشت
    if selected_room is None:
        print("otagh mored nazar payda nashod")
        input("baraye edame ENTER bezanid")
        return

    # بررسی ظرفیت اتاق
    if guests > selected_room["capacity"]:
        print("tedad nafarat bishtar az zarfiat ast")
        input("baraye edame ENTER bezanid")
        return

    total_cost = selected_room["total_price"][1]

    # بررسی و انجام پرداخت
    if not user.pay(total_cost):
        print("etebar shoma kafi nist!")
        input("baraye edame ENTER bezanid")
        return

    update_user(user)

    # ساخت شیء رزرو
    reservation = Reservation(
        user.username,
        selected_room["room_id"],
        check_in,
        check_out,
        guests,
        total_cost
    )

    # صدور فاکتور
    create_invoice(reservation)
    
    # ذخیره رزرو در فایل
    reservations = load_reservations()
    reservations.append(reservation.to_dict())
    save_reservations(reservations)

    print("rezerv ba movafaghiyat anjam shod")
    print(f"etebar baghimande shoma: {user.balance}")
    input("baraye edame ENTER bezanid")
