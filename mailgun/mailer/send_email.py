import os
import requests
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

def send_email(to_email, subject, template_name, context, attachment_filename):
    template = env.get_template(template_name)
    html_content = template.render(context)

    data={
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }

    if attachment_filename:
        path = os.path.join(ATTACHMENTS_DIR, attachment_filename)
        with open(path, "rb") as pdf:
            files = [("attachment", pdf)]
            response = requests.post(
                f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                auth=("api", MAILGUN_API_KEY),
                files=files,
                data=data
            )
    else:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=data
        )

    return response
