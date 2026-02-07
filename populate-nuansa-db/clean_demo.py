from config import db

if __name__ == "__main__":
    seats = db.collection("seats")
    for doc in seats.stream():
        s = doc.id
        if not s.startswith("level-1_D") or not len(s) == 11:
            seats.document(s).delete()
            print(f"deleted {s}")
