import json


def load_users():
    # خواندن کاربران از فایل
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # اگر فایل خالی یا خراب بود
        return []


def save_users(users_list):
    # ذخیره کاربران در فایل
    with open("users.json", "w") as file:
        json.dump(users_list, file, indent=4)
