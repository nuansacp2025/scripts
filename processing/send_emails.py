import asyncio
import aiohttp
from ..db import get_unconfirmed_purchases
from ..mailgun import send_confirmation_email

async def send_confirmation_emails(session: aiohttp.ClientSession):
    order_docs = get_unconfirmed_purchases()

    tasks = [
        send_confirmation_email(
            session,
            doc.get("email"),
            doc.get("code"),
            doc.reference
        ) for doc in order_docs
    ]
    await asyncio.gather(*tasks)
