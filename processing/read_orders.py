import csv
from collections import defaultdict

def read_orders(csv_file_path):
    email_to_ids = defaultdict(list)
    id_to_category = {}

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        row_id = 1
        for row in reader:
            email = row["Email"]
            product_name = row["Product Name"]

            email_to_ids[email].append(row_id)
            id_to_category[row_id] = product_name

            row_id += 1

    return email_to_ids, id_to_category