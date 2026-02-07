from config import db
from google.cloud.firestore import SERVER_TIMESTAMP
from firebase_admin.firestore import firestore

if __name__ == "__main__":
    ticket = {
        "code": "DDAY_4A_1740",
        "catA": 4,
        "catB": 0,
        "catC": 0,
        "seatConfirmed": False,
        "checkedIn": False,
        "customerEmail": "nuansacp.tech@gmail.com",
        "lastUpdated": SERVER_TIMESTAMP,
        "createdAt": SERVER_TIMESTAMP,
        "purchaseConfirmationSent": True,
    }
    _, ref = db.collection("tickets").add(ticket)
    ticket_id = ref.id
    print(ticket_id)
    input()
    db.collection("customers").document("0bOQA9zUTn5Y8LKXnwDN").update({
        "ticketIds": firestore.ArrayUnion([ticket_id]),
        "lastUpdated": SERVER_TIMESTAMP
    })
    """
    seats = [f"level-1_FF{i}" for i in range(4,37)] + [f"level-1_GG{i}" for i in range(5,37) if i not in [20, 21]] + [f"level-2_E{i}" for i in range(4,38)] + [f"level-2_F{i}" for i in range(3,38)] + [f"level-2_G{i}" for i in range(5,37)]
    assert len(seats) == 63 + 101

    for s_id in seats:
        ref = db.document("seats", s_id)
        ref.update({
            "isAvailable": False,
            "reservedBy": "YkPlX1RDAWNBwAY3njr0",
            "lastUpdated": SERVER_TIMESTAMP,
        })
    isAvailableCache = db.document("caches", "seats.isAvailable")
    isAvailableCache.update({s_id: False for s_id in seats})
    """
