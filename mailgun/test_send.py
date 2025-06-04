from .mailer.send_email import send_email

send_email(
    to_email="sandykristianwaluyo3@gmail.com",
    subject="NUANSA 2025 Ticket Purchase Confirmation",
    template_name="purchase.html",
    context={
        "ticket_code": "NUA2025-001",
        "login_link": "https://tickets.nuansacp.org"
    }
)

send_email(
    to_email="sandykristianwaluyo3@gmail.com",
    subject="NUANSA 2025 Seat Confirmation",
    template_name="seat_confirmation.html",
    context={
        "ticket_code": "NUA2025-001",
        "share_link": "https://tickets.nuansacp.org",
        "seat_num": "EJAY-LoL234"
    }
)

send_email(
    to_email="sandykristianwaluyo3@gmail.com",
    subject="Reminder: Choose Your Seat for NUANSA 2025",
    template_name="seat_select_reminder.html",
    context={
        "ticket_code": "NUA2025-001",
        "login_link": "https://tickets.nuansacp.org"
    }
)

send_email(
    to_email="sandykristianwaluyo3@gmail.com",
    subject="Thank You",
    template_name="farewell.html",
    context={
        "feedback_link": "https://feedback.nuansacp.org"
    }
)