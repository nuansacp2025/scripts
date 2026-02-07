from config import db

if __name__ == "__main__":
    tickets = db.collection("tickets")
    for doc in tickets.stream():
        t = doc.id
        data = doc.to_dict()
        upd = {}
        if "checkedIn" not in data:
            upd["checkedIn"] = False
        if "seatConfirmed" not in data:
            upd["seatConfirmed"] = False
        if len(upd) > 0:
            tickets.document(t).update(upd)
            print(f"updated {t}: {upd}")
