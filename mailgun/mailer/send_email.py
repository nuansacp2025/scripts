import asyncio
import os
import requests
import time
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
FROM_EMAIL = os.getenv("FROM_EMAIL")


# base dirs
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "attachments")

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

def send_email(to_email, subject, template_name, context, attachments=None, timeout=5):
    template = env.get_template(template_name)
    html_content = template.render(context)

    data = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    files = [("attachment", f) for f in attachments] if attachments is not None else None

    # Possible API response codes: 400, 403, 404, 429, 500
    # https://documentation.mailgun.com/docs/mailgun/api-reference/#api-response-codes

    start_time = time.time()
    retry_interval = 0.1
    while True:
        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                auth=("api", MAILGUN_API_KEY),
                files=files,
                data=data,
                timeout=timeout
            )
        except requests.Timeout:
            raise RuntimeError("Request timed out")
        if response.status_code == 200:
            return response
        elif response.status_code in (429, 500):
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise RuntimeError("Request timed out after retries")
            sleep_time = min(retry_interval, timeout - elapsed)
            time.sleep(sleep_time)
            retry_interval *= 2
            continue
        else:
            response.raise_for_status()
