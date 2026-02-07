from config import db

if __name__ == "__main__":
    #coll = db.collection("tickets")
    coll = db.collection("customers")
    for doc in coll.stream():
        i = doc.id
        #if i == "3LtLYlsDMjLT09iFmrwz": continue
        if i == "0bOQA9zUTn5Y8LKXnwDN": continue
        coll.document(i).delete()
        print(f"deleted {i}")
