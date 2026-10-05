import imaplib
import email
from email.header import decode_header

def get_latest_email():

    EMAIL = "hariomkamble8530@gmail.com"
    PASSWORD = "enop vypf owbo qwxd"

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)

    mail.select("inbox")

    status, messages = mail.search(None, "ALL")

    email_ids = messages[0].split()
    latest_email_id = email_ids[-1]

    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):

            msg = email.message_from_bytes(response_part[1])

            subject, encoding = decode_header(msg["Subject"])[0]

            if isinstance(subject, bytes):
                subject = subject.decode()

            sender = msg.get("From")

            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()

                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            header = str(msg)

            return subject, sender, body, header