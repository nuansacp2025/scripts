import csv
from .generate_code import generate_ticket_id

def read_orders(csv_file_path):
    orders = {}
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Status"] != "Paid": # Ignore unpaid orders
                continue

            order_id = row["Order"]
            date_time = row["Created Date"]
            email = row["Email"]
            cat = row["Product Name"]
            qty = row["Quantity"]

            ticket_id = generate_ticket_id(order_id, date_time)
            key = (ticket_id, email)

            if key not in orders:
                orders[key] = {}

            if cat not in orders[key]:
                orders[key][cat] = 0

            orders[key][cat] += qty
    
    return orders


