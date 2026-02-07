import json
from config import db

if __name__ == "__main__":
    with open("updated_seats_lv2.json", "r") as f:
        objs = json.load(f)
    seats = db.collection("seats")
    cnt = 0
    for seat in objs:
        if "label" in seat and "level" in seat:
            seat_id = f'{seat["level"]}_{seat["label"]}'
            seats.document(seat_id).set(seat, merge=True)
            print(seat_id, "updated")
            cnt += 1
    print(cnt)
