import asyncio
import os
from .processing import process_orders

if __name__ == "__main__":
    asyncio.run(process_orders(os.path.join(os.path.dirname(__file__), "edit.csv")))