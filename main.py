from user_manager import register, login,add_balance
from room_manager import (
    load_rooms,
    show_rooms,
    filter_by_type,
    filter_by_price,
    filter_by_amenities
)
from reservation_manager import (
search_available_rooms,
create_reservation,
show_user_reservations,
cancel_reservation
)

import os

os.system("color 80")

# auth menu (login / register)

def auth_menu():
    while True:
        os.system("cls")
        print("=== menu asli ===")
        print("1. sabt nam")
        print("2. vorood")
        print("3. khorooj")

        choice = input("entekhab shoma: ")
        os.system("cls")

        if choice == "1":
            register()

        elif choice == "2":
            user = login()
            if user is not None:
                return user

        elif choice == "3":
            print("az barname khareg shodid")
            return None

        else:
            print("entekhab na motabar!")
            input("ENTER baraye edame...")


# room menu 

def room_menu(user):
    while True:
        os.system("cls")
        print("=== menu otagh ha ===")
        print("1. namayesh etelaat hame otagh ha")
        print("2. jostojo otagh bar asas tarikh")
        print("3. filter otagh ha")
        print("4. reserve otagh ")
        print("5. namayesh rezerv haye man")        
        print("6. namayesh rezerv haye faal")      
        print("7. laghv rezerv") 
        print("8. afzayesh etebar")
        print("9. khorooj az hesab")

        choice = input("entekhab shoma: ")
        os.system("cls")

        if choice == "1":
            rooms = load_rooms()
            show_rooms(rooms)

        elif choice == "2":
            search_by_date_menu()

        elif choice == "3":
            filter_menu()

        elif choice == "4":
            create_reservation(user)   

        elif choice == "5":
            show_user_reservations(user)

        elif choice == "6":
            show_user_reservations(user, "active")

        elif choice == "7":
            cancel_reservation(user)
     
        elif choice == "8":
            add_balance(user)

        elif choice == "9":
            print("az hesab khareg shodid")
            break

        else:
            print("entekhab na motabar!")
            input("ENTER baraye edame...")


# filter menu

def filter_menu():
    while True:
        os.system("cls")
        print("=== filter otagh ha ===")
        print("1. filter bar asas noe otagh")
        print("2. filter bar asas gheymat")
        print("3. filter bar asas emkanat")
        print("4. bazgasht")

        choice = input("entekhab shoma: ")
        os.system("cls")

        if choice == "1":
            room_type = input("noe otagh (1 takhte / 2 takhte / Suite): ")
            rooms = filter_by_type(room_type)
            show_rooms(rooms)
            

        elif choice == "2":
            min_price = int(input("hadeaghal gheymat: "))
            max_price = int(input("hadeaksar gheymat: "))
            rooms = filter_by_price(min_price, max_price)
            show_rooms(rooms)
            

        elif choice == "3":
            amenities = input("emkanat mored nazar ra ba , joda konid: ")
            amenities_list = []
            for a in amenities.split(","):
                amenities_list.append(a.strip())

            show_rooms(filter_by_amenities(amenities_list))
            

        elif choice == "4":
            break

        else:
            print("entekhab na motabar!")
            input("ENTER baraye edame...")



# search by date menu 

def search_by_date_menu():
    os.system("cls")
    print("=== jostojo bar asas tarikh ===")
    
    check_in = input("tarikh vorood (YYYY-MM-DD): ")
    check_out = input("tarikh khorooj (YYYY-MM-DD): ")

    available_rooms = search_available_rooms(check_in, check_out)

    print("\n--- otagh haye ghabel rezerv---")
    for room in available_rooms:
        print(
            f"otagh: {room['room_id']} | "
            f"zarfiyat: {room['capacity']} | "
            f"ghaymat kol: {room['total_price']}"
        )
    
    input("ENTER baraye bazgasht...")



# main

def main():
    print("khosh amadid")
    while True:
        user = auth_menu()
        if user is None:
            break
        room_menu(user)


if __name__ == "__main__":
    main()
