import aiohttp
import asyncio

from .mailer import send_email, send_purchase_confirmation, send_seat_confirmation
from ..db.db import db
from ..processing import TicketPDFGenerator

async def main():
    async with aiohttp.ClientSession() as session:
        """
        await send_purchase_confirmation(
            session=session,
            ticket_ref=db.document("tickets", "3LtLYlsDMjLT09iFmrwz"),
        )
        """
        await send_seat_confirmation(
            session=session,
            ticket_ref=db.document("tickets", "3LtLYlsDMjLT09iFmrwz"),
            pdf_generator=TicketPDFGenerator(),
        )

if __name__ == "__main__":
    asyncio.run(main())


# send_email(
#     to_email="sandykristianwaluyo3@gmail.com",
#     subject="Reminder: Choose Your Seat for NUANSA 2025",
#     template_name="seat_select_reminder.html",
#     context={
#         "ticket_code": "NUA2025-001",
#         "login_link": "https://tickets.nuansacp.org"
#     }
# )
#
# send_email(
#     to_email="sandykristianwaluyo3@gmail.com",
#     subject="Thank You",
#     template_name="farewell.html",
#     context={
#         "feedback_link": "https://feedback.nuansacp.org"
#     }
# )