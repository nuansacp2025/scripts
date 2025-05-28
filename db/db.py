import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('credential.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

def add_orders(orders):
    # Assumption: the cat_dict keys are catA, catB, catC following the naming in firestore
    for key, cat_dict in orders.items():
        ticket_id, email = key
        ticket = cat_dict.copy()
        if "catA" not in ticket:
            ticket["catA"] = 0
        if "catB" not in ticket:
            ticket["catB"] = 0
        if "catC" not in ticket:
            ticket["catC"] = 0
        ticket["code"] = ticket_id
        ticket["checkedIn"] = False
        ticket["seatConfirmed"] = False
        print(ticket)
        _, ref = db.collection("tickets").add(ticket)
        _, _ = db.collection("customers").add({
            "email": email,
            "ticketId": ref.id
        })
