# مدیریت خواندن و نمایش اتاق‌ها

import json
from room import StandardRoom, SuiteRoom, Room


def load_rooms():
    try:
        with open("rooms.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

def load_rooms_obj():
    room_list = []

    for room in load_rooms():
        if room['room_type'] in ['1 takhte', '2 takhte']:
            obj = StandardRoom(
                room['room_id'], room['room_type'], room['price_per_night'],
                room['amenities'], room['capacity']
            )
        elif room['room_type'] == 'Suite':
            obj = SuiteRoom(
                room['room_id'], room['room_type'], room['price_per_night'],
                room['amenities'], room['capacity']
            )
        else:
            obj = Room(
                room['room_id'], room['room_type'], room['price_per_night'],
                room['amenities'], room['capacity']
            )
        
        room_list.append(obj)
    return room_list


def save_rooms(rooms):
    with open("rooms.json", "w") as file:
        json.dump(rooms, file, indent=4)



def show_rooms(rooms):

    if not rooms:
        print("hich otaghi vojood nadarad")
    else:
        print("\n--- list otagh ha---")
        print(
            f"{'ID':<6} | "
            f"{'NOE':<10} | "
            f"{'GHEYMAT/SHAB':<15} | "
            f"{'ZARFIYAT':<8} | "
            f"{'EMKANAT'}"
        )
        print("-" * 65)

        for room in rooms:
             print(
                f"{room['room_id']:<6} | "
                f"{room['room_type']:<10} | "
                f"{room['price_per_night']:<15} | "
                f"{room['capacity']:<8} | "
                f"{', '.join(room['amenities'])}"
            )

        print("=" * 65)

    input('baraye edame ENTER bezanid')
    return

def filter_by_type(room_type):      # فیلتر بر اساس نوع اتاق

    rooms = load_rooms()
    filtered_rooms = []     

    for room in rooms:    
        if room["room_type"] == room_type:
            filtered_rooms.append(room)

    return filtered_rooms   



def filter_by_price(min_price, max_price):      # فیلتر بر اساس قیمت

    rooms = load_rooms()
    filtered_rooms = []

    for room in rooms:
        if min_price <= room["price_per_night"] <= max_price:
            filtered_rooms.append(room)

    return filtered_rooms


def filter_by_amenities(required_amenities):        # فیلتر بر اساس امکانات

    rooms = load_rooms()
    filtered_rooms = []

    for room in rooms:
        assumption = True  

        for i in required_amenities:
            if i not in room["amenities"]:
                assumption = False
                break

        if assumption:
            filtered_rooms.append(room)

    return filtered_rooms
