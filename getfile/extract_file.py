import imaplib
import email
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
user = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using credentials
my_mail.login(user, password)

# Select Inbox
my_mail.select('Inbox')

# Time
today = datetime.now()
yesterday = today - timedelta(days=1)
yesterday_date_string = yesterday.strftime("%Y-%m-%d")

# Create folder
folder_name = today.strftime(f"Mail_Attachments")
if not os.path.exists(folder_name):
    os.makedirs(folder_name, mode=0o777)
folder_path = os.path.abspath(folder_name)

# Filter
# To be replaced with NUSFastPay's email
search_query = f'(X-GM-RAW "has:attachment after:{yesterday_date_string} from:sandykristianwaluyo3@gmail.com")'
_, data = my_mail.search(None, search_query)

print(data)

mail_id_list = data[0].split() # IDs of all emails we want to fetch

raw_emails = [] # Empty list to capture all messages
for num in mail_id_list:
    typ, data = my_mail.fetch(num, '(RFC822)') # Fetch the whole message
    raw_emails.append(data)


for raw_email in raw_emails:
    for response_part in raw_email:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filepath = os.path.join(folder_path, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))


my_mail.logout()