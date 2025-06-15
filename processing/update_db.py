from ..db import insert_order

def add_orders(orders):
    for key, cat_dict in orders.items():
        ticket_code, email = key
        insert_order(ticket_code, email, cat_dict)
