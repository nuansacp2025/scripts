import os
from mailgun import Mailgun
from dotenv import load_dotenv

load_dotenv()  # loads .env

mg = Mailgun(
    domain=os.getenv("MAILGUN_DOMAIN"),
    api_key=os.getenv("MAILGUN_API_KEY")
)

