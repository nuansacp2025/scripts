import io
import os
import aiohttp
import asyncio
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

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

INLINE_IMAGES_FILENAMES = ["nuansa-logo.png"]
INLINE_IMAGES = {}
for fname in INLINE_IMAGES_FILENAMES:
    with open(os.path.join(TEMPLATE_DIR, f"images/{fname}"), "rb") as f:
        INLINE_IMAGES[fname] = io.BytesIO(f.read())

async def send_email(session: aiohttp.ClientSession, to_email, subject, template_name, context, attachments=None, timeout=5):
    template = env.get_template(template_name)
    html_content = template.render(context)

    data = aiohttp.FormData()
    data.add_fields(
        ("from", FROM_EMAIL),
        ("to", to_email),
        ("subject", subject),
        ("html", html_content),
    )
    for fname in INLINE_IMAGES:
        data.add_field("inline", INLINE_IMAGES[fname], filename=fname)
    if attachments:
        for fname, f in attachments:
            data.add_field("attachment", f, filename=fname)

    # Possible API response codes: 400, 403, 404, 429, 500
    # https://documentation.mailgun.com/docs/mailgun/api-reference/#api-response-codes

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    start_time = time.perf_counter()
    retry_interval = 0.1
    while True:
        try:
            async with session.post(
                url,
                auth=aiohttp.BasicAuth('api', MAILGUN_API_KEY),
                data=data,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                status = response.status
                if status == 200:
                    return response
                elif status in (429, 500):
                    elapsed = time.perf_counter() - start_time
                    if elapsed >= timeout:
                        raise RuntimeError("Request timed out after retries")
                    sleep_time = min(retry_interval, timeout - elapsed)
                    await asyncio.sleep(sleep_time)
                    retry_interval *= 2
                else:
                    response.raise_for_status()
        except asyncio.TimeoutError:
            raise RuntimeError("Request timed out")
