from config import db

if __name__ == "__main__":
    seats = db.collection("seats")
    for i in range(20):
        s = f"level-1_D{i+11}"
        doc = seats.document(s)
        doc.update({
            "label": f"D{i+11}",
            "level": "level-1",
            "category": ("catA" if i < 5 else "catB" if i < 15 else "catC"),
            "notSelectable": False,
        })
        if i != 0:
            doc.update({
                "leftId": f"level-1_D{i+10}"
            })
        if i != 19:
            doc.update({
                "rightId": f"level-1_D{i+12}"
            })
