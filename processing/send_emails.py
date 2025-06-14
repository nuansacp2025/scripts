import aiohttp
from ..db import get_unconfirmed_tickets
from ..mailgun import send_confirmation_email

async def send_confirmation_emails(session: aiohttp.ClientSession):
    order_docs = get_unconfirmed_tickets()

    for doc in order_docs:
        ref = doc.reference
        email = doc.get("email")
        ticket_id = doc.get("code")

        await send_confirmation_email(session, email, ticket_id, ref)
