from datetime import datetime

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def generate_ticket_id(order_id: str, datetime_str: str) -> str:
    """
    Generates a unique 9-character ticket ID by combining the last 4 digits 
    of the order ID with a 5-character code derived from the datetime.

    Args:
        order_id (str): Order identifier (e.g., "ORD0012345").
        datetime_str (str): Datetime in "D/M/YYYY h:mm:ss AM/PM" format 
                            (e.g., "3/10/2023 4:25:42 PM").

    Returns:
        str: A unique 9-character ticket ID (e.g., "2164w3WUf").
    """
    last4 = order_id[-4:]
    code = datetime_to_code(datetime_str)
    return code + last4

def to_base62(num: int, length: int = 5) -> str:
    result = ""
    while num > 0:
        result = BASE62[num % 62] + result
        num //= 62
    return result.rjust(length, '0')

def datetime_to_code(date_time_str: str) -> str:
    dt = datetime.strptime(date_time_str, "%d/%m/%Y %I:%M:%S %p")
    month = dt.month     # 1–12 → 4 bits
    day = dt.day         # 1–31 → 5 bits
    hour = dt.hour       # 0–23 → 5 bits
    minute = dt.minute   # 0–59 → 6 bits
    second = dt.second   # 0–59 → 6 bits

    # Combine into a single integer 26 bits
    code = (month << 22) | (day << 17) | (hour << 12) | (minute << 6) | second

    # Convert 26 bit to 5 base-62 characters
    return to_base62(code, 5)
