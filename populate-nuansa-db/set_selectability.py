from config import db
from google.cloud.firestore import SERVER_TIMESTAMP, DELETE_FIELD

if __name__ == "__main__":
    seats = [f"level-1_FF{i}" for i in range(4,37)] + [f"level-1_GG{i}" for i in range(5,37) if i not in [20, 21]] + [f"level-2_E{i}" for i in range(4,38)] + [f"level-2_F{i}" for i in range(3,38)] + [f"level-2_G{i}" for i in range(5,37)]
    assert len(seats) == 63 + 101

    for s_id in seats:
        ref = db.document("seats", s_id)
        ref.update({
            "isAvailable": True,
            "reservedBy": DELETE_FIELD,
            "lastUpdated": SERVER_TIMESTAMP,
        })
    isAvailableCache = db.document("caches", "seats.isAvailable")
    isAvailableCache.update({s_id: False for s_id in seats})
