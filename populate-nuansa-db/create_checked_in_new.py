from config import db

if __name__ == "__main__":
    seats = db.collection("seats")
    seat_ids = [doc.id for doc in seats.stream()]
    checked_in_cache = db.collection("caches").document("seats.checkedIn")
    checked_in_cache.set({i: False for i in seat_ids})
