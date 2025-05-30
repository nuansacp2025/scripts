import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

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
        _, ref = db.collection("tickets").add(ticket)
        cache = db.collection("customers").where(filter=FieldFilter("email", "==", email)).stream()
        cache_id = None
        cache_dict = None
        for doc in cache:
            cache_id = doc.id
            cache_dict = doc.to_dict()
        if not cache_id:
            _, _ = db.collection("customers").add({
                "email": email,
                "ticketIds": [ref.id]
            })
        else:
            db.collection("customers").document(cache_id).update({"ticketIds": cache_dict["ticketIds"] + [ref.id]})
