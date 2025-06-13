import os
import json
import aiohttp
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore import SERVER_TIMESTAMP
from ..mailgun import send_email
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

async def add_orders(orders):    
    # Assumption: the cat_dict keys are catA, catB, catC following the naming in firestore
    async with aiohttp.ClientSession() as session:
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
            ticket["purchaseConfirmationSent"] = False
            ticket["lastUpdated"] = SERVER_TIMESTAMP
            ticket["createdAt"] = SERVER_TIMESTAMP

            try:
                _, ref = db.collection("tickets").add(ticket)
                add_order_to_customer(transaction, email, ref)
            except Exception as e:
                print(f"Failed to insert ticket to DB: {e}")
                continue

            subject = "Confirmation: Your Ticket and Login Details"
            template_name = "purchase.html"
            context = {
                "ticket_code": ticket_id,
                "login_link": BASE_URL + "/login"
            }

            try:
                response = await send_email(session, email, subject, template_name, context)
                if response.status == 200:
                    ref.update({"purchaseConfirmationSent": True})
            except Exception as e:
                print(f"Email failed to {email}: {e}")
