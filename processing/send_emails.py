import asyncio
import aiohttp
from ..db import get_unconfirmed_purchases, get_confirmed_tickets
from ..mailgun.mailer import send_purchase_confirmation, send_seat_confirmation
from .generate_ticket_pdf import TicketPDFGenerator

async def send_confirmation_emails(session: aiohttp.ClientSession):
    pdf_generator = TicketPDFGenerator()

    # TODO: if possible, check the number of email quotas (x) already used up on that day, then set limit = 100 - x
    limit = 100

    print("Begin processing seat confirmation emails...")

    confirmed_ticket_docs_stream = get_confirmed_tickets(limit)
    seat_confirmation_tasks = []
    for snap in confirmed_ticket_docs_stream:
        seat_confirmation_tasks.append(send_seat_confirmation(session, snap.reference, pdf_generator))

    print("Done.")

    limit -= len(seat_confirmation_tasks)

    print("Begin processing purchase confirmation emails...")

    order_docs_stream = get_unconfirmed_purchases(limit)
    purchase_confirmation_tasks = []
    for snap in order_docs_stream:
        purchase_confirmation_tasks.append(send_purchase_confirmation(session, snap.reference))

    print("Done.")

    print("Awaiting all emails...")

    await asyncio.gather(*seat_confirmation_tasks, *purchase_confirmation_tasks)
