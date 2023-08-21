from utils import getenv
import requests
import rq


def send_simple_message(to, subject, body):
    domain = getenv("MAILGUN_DOMAIN")
    key = getenv("MAILGUN_API_KEY")

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", key),
        data={"from": f"App <mailgun@{domain}>",
              "to": [to],
              "subject": subject,
              "text": body})


def send_user_registration_email(email, username):
    return send_simple_message(email, "Successfully signed up", f"Hi {username}! You have sucessfully signed up to the Stores REST API.")
