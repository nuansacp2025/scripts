from ..db import insert_ticket

def add_orders(orders):
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

        insert_ticket(ticket, email)