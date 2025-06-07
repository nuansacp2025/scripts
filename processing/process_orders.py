import csv
import re
from .generate_code import generate_ticket_id
from db import add_orders
from getfile import extract_file
from mailgun import send_email

def process_orders():
    csv_contents = extract_file()

    for csv_content in csv_contents:
        orders = read_orders(csv_content)
        add_orders(orders)

def read_orders(csv_content):
    orders = {}

    decoded = csv_content.decode('utf-8-sig')
    file = io.StringIO(decoded)
    reader = csv.DictReader(file)

    for row in reader:
        if row["Booking Status"] != "Paid":  # Ignore unpaid orders
            continue

        order_id = row["Receipt"]
        date_time = row["Paid Date"]
        email = row["Email"]

        order_description = row["Line Description"]
        cat, qty = parse_order_description(order_description)
        cat = "cat" + cat

        ticket_id = generate_ticket_id(order_id, date_time)
        key = (ticket_id, email)

        if key not in orders:
            orders[key] = {}

        if cat not in orders[key]:
            orders[key][cat] = 0

        orders[key][cat] += qty

    return orders

def parse_order_description(line_description):
    match = re.search(r'Category ([A-Z]): (\d+) pax', line_description)
    if match:
        return match.group(1), int(match.group(2))
    return None


