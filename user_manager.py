from user import User
from file_manager import load_users, save_users

def register():
    print("=== sabte nam ===")

    first_name = input("nam: ")
    last_name = input("nam khanevadegy: ")
    username = input("nam karbari: ")
    password = input("ramz oboor: ")

    users = load_users()

    # بررسی تکراری نبودن نام کاربری
    for u in users:
        if u["username"] == username:
            print("in nam karbari ghablan sabt shode!")
            return
        

    new_user = User(first_name, last_name, username, password)

    users.append(new_user.to_dict())
    save_users(users)

    print("sabt nam ba movafaghyat anjam shod")
    input('baraye edame ENTER bezanid')


def login():
    print("=== vorood ===")

    username = input("nam karbari: ")
    password = input("ramz oboor: ")

    users = load_users()

    for u in users:
        if u["username"] == username and u["password"] == password:
            user_obj = User.from_dict(u)
            print(f" {u['first_name']} aziz khosh amadi")
            input('baraye edame ENTER bezanid')
            return user_obj

    print("nam karbari ya ramz oboor eshtebah ast!")
    input('baraye edame ENTER bezanid')
    return None


# افزایش اعتبار
def add_balance(user):
    print("=== afzayesh etebar ===")
    
    # نمایش موجودی فعلی
    print(f"etebar feli shoma: {user.balance}")

    try:
        amount = int(input("mablaghi ke mikhahid ezafe konid: "))
    except ValueError:
        print("mablagh bayad adad sahih bashad!")
        input('baraye edame ENTER bezanid')
        return

    # بررسی منفی یا صفر بودن مبلغ
    if amount <= 0:
        print("mablagh namotabar ast, bayad bishtar az sefr bashad.")
        input('baraye edame ENTER bezanid')
        return

    user.add_balance(amount)

    # به‌روزرسانی فایل users.json
    users = load_users()
    for u in users:
        if u["username"] == user.username:
            u["balance"] = user.balance
            break

    save_users(users)

    print("\netebar shoma ba movafaghiyat afzayesh yaft!")
    print(f"etebar jadid shoma: {user.balance}")
    input('baraye edame ENTER bezanid')


#  ذخیره تغییرات کاربر
def update_user(user):
    users = load_users()

    for u in users:
        if u["username"] == user.username:
            u.clear()
            u.update(user.to_dict())
            break

    save_users(users)

    