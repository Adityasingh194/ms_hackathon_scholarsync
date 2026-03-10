import requests
from ..config import SENDGRID_API_KEY, EMAIL_SENDER


def send_email(data):

    to = data["to"]
    subject = data["subject"]
    body = data["body"]

    print("[MCP] send_email ->", to)

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "personalizations": [{"to": [{"email": to}]}],
        "from": {"email": EMAIL_SENDER},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}]
    }

    r = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers=headers,
        json=payload
    )

    if r.status_code == 202:
        return {"result": "Email accepted by SendGrid"}

    return {"result": f"SendGrid error: {r.text}"}