import asyncio
import aiohttp
from ..db import get_unconfirmed_purchases
from ..mailgun import send_purchase_confirmation

async def send_confirmation_emails(session: aiohttp.ClientSession):
    order_docs = get_unconfirmed_purchases()

    tasks = [
        send_purchase_confirmation(
            session,
            doc.get("customerEmail"),
            doc.get("code"),
            doc.reference
        ) for doc in order_docs
    ]
    await asyncio.gather(*tasks)
