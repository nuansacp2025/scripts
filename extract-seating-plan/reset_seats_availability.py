from config import db
from google.cloud.firestore import SERVER_TIMESTAMP, DELETE_FIELD

if __name__ == "__main__":
    tickets = db.collection("tickets")
    seats = db.collection("seats")
    is_available_cache = db.collection("caches").document("seats.isAvailable")

    for doc in tickets.stream():
        ticket_id = doc.id
        tickets.document(ticket_id).update({
            "seatConfirmed": False,
            "confirmedAt": DELETE_FIELD,
            "seatConfirmationSent": DELETE_FIELD,
            "lastUpdated": SERVER_TIMESTAMP,
        })
        print("ticket", ticket_id, "updated")

    cache_update = {}
    for doc in seats.stream():
        seat_id = doc.id
        seats.document(seat_id).update({
            "isAvailable": True,
            "reservedBy": DELETE_FIELD,
            "lastUpdated": SERVER_TIMESTAMP,
        })
        cache_update[seat_id] = True
        print("seat", seat_id, "updated")

    is_available_cache.update(cache_update)
    print("cache updated")

    print("done")
