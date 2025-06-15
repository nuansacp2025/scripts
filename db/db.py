import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import SERVER_TIMESTAMP
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

cred_json_str = os.getenv('PY_CREDENTIAL_JSON')

if not cred_json_str:
    raise ValueError("Environment variable PY_CREDENTIAL_JSON not set")

cred_json = json.loads(cred_json_str)

cred = credentials.Certificate(cred_json)

app = firebase_admin.initialize_app(cred)

db = firestore.client()
transaction = db.transaction()

@firestore.transactional
def add_order_to_customer(transaction, email, ticket_ref):
    ref = db.collection("customers")
    query = list(ref.where(filter=FieldFilter("email", "==", email)).get(transaction=transaction))
    if not query:
        newRef = db.collection("customers").document()
        transaction.set(newRef, {
            "email": email, 
            "ticketIds": [ticket_ref.id],
            "lastUpdated": SERVER_TIMESTAMP
        })
    else:
        transaction.update(query[0].reference, {
            "ticketIds": firestore.ArrayUnion([ticket_ref.id]),
            "lastUpdated": SERVER_TIMESTAMP
        })

def insert_order(ticket_code, email, cat_dict):
    ticket = cat_dict.copy()
    for cat in ["catA", "catB", "catC"]:
        if cat not in ticket:
            ticket[cat] = 0

    ticket["code"] = ticket_code
    ticket["customerEmail"] = email
    ticket["checkedIn"] = False
    ticket["seatConfirmed"] = False

    ticket["purchaseConfirmationSent"] = False
    ticket["createdAt"] = SERVER_TIMESTAMP
    ticket["lastUpdated"] = SERVER_TIMESTAMP

    try:
        _, ref = db.collection("tickets").add(ticket)
        add_order_to_customer(transaction, email, ref)

    except Exception as e:
        print(f"Failed to insert ticket to DB: {e}")

    return ref

def get_seats(ticket_id):
    return db.collection("tickets").where("reservedBy", "==", ticket_id).stream()

def get_confirmed_tickets(limit=None):
    if limit == 0: return []
    try:
        query = (
            db.collection("tickets")
            .where("seatConfirmationSent", "==", False)
            .order_by("confirmedAt", direction=firestore.Query.ASCENDING)
        )
        if limit:
            query = query.limit(limit)
        return query.stream()

    except Exception as e:
        print(f"Error querying tickets for unsent seat confirmation: {e}")
        return []

def get_unconfirmed_purchases(limit=None):
    if limit == 0: return []
    try:
        query = (
            db.collection("tickets")
            .where("purchaseConfirmationSent", "==", False)
            .order_by("createdAt", direction=firestore.Query.ASCENDING)
        )
        if limit:
            query = query.limit(limit)
        return query.stream()

    except Exception as e:
        print(f"Error querying tickets for unsent purchase confirmation: {e}")
        return []
