from ..db import insert_ticket

def add_orders(orders):
    for key, cat_dict in orders.items():
        ticket_code, email = key
        insert_ticket(ticket_code, email, cat_dict)
