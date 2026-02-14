def create_invoice(reservation):
    filename = f"invoice_{reservation.username}_{reservation.room_id}_{reservation.check_in}.txt"

    with open(filename, "w") as file:
        file.write("=== FACTOR REZERV OTAGH ===\n")
        file.write(f"nam karbar: {reservation.username}\n")
        file.write(f"shomare otagh: {reservation.room_id}\n")
        file.write(f"tarikh vorood: {reservation.check_in}\n")
        file.write(f"tarikh khorooj: {reservation.check_out}\n")
        file.write(f"tedad nafarat: {reservation.guests}\n")
        file.write(f"mablagh kol: {reservation.total_cost}\n")
        file.write("===========================\n")
