import io
import os
import csv
import re
import json
import aiohttp
from .update_db import add_orders
from .send_emails import send_confirmation_emails
from .generate_code import generate_ticket_id
from ..getfile import extract_file

with open(os.path.join(os.path.dirname(__file__), "assets/data/bundle_mapping.json"), "r") as f:
    BUNDLE_DICT = json.load(f)

async def process_orders(filepath=None):
    async with aiohttp.ClientSession() as session:
        csv_contents = extract_file(filepath=filepath)

        for csv_content in csv_contents:
            orders = read_orders(csv_content)
            add_orders(orders)

        await send_confirmation_emails(session)

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
        
        try:
            cat, qty = parse_order_description(order_description)
        except Exception as e:
            print(f"Failed to parse order description: {e}")

        qty = qty * int(float(row["Quantity"]))

        ticket_id = generate_ticket_id(order_id, date_time)
        key = (ticket_id, email)

        if key not in orders:
            orders[key] = {}

        if cat not in orders[key]:
            orders[key][cat] = 0

        orders[key][cat] += qty

    return orders

def parse_order_description(line_description):
    if line_description not in BUNDLE_DICT:
        raise KeyError(f"Invalid order description: '{line_description}'")

    return BUNDLE_DICT[line_description]


