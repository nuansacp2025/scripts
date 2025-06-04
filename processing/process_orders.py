import csv
from .generate_code import generate_ticket_id
from db import add_orders
from getfile import extract_file
from mailgun import send_email

def process_orders():
    csv_contents = extract_file()

    for csv_content in csv_contents:
        orders = read_orders(csv_content)
        add_orders(orders)
        # TODO: send email to confirm purchase

def read_orders(csv_content):
    orders = {}

    decoded = csv_content.decode('utf-8-sig')
    file = io.StringIO(decoded)
    reader = csv.DictReader(file)

    for row in reader:
        if row["Status"] != "Paid":  # Ignore unpaid orders
            continue

        order_id = row["Order"]
        date_time = row["Created Date"]
        email = row["Email"]
        cat = row["Product Name"]
        qty = int(row["Quantity"])  # Ensure it's an integer

        ticket_id = generate_ticket_id(order_id, date_time)
        key = (ticket_id, email)

        if key not in orders:
            orders[key] = {}

        if cat not in orders[key]:
            orders[key][cat] = 0

        orders[key][cat] += qty

    return orders


