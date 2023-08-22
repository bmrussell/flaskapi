from utils import getenv
import requests
import jinja2

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)


def render_template(filename, **context):
    return template_env.get_template(filename).render(**context)

def send_simple_message(to, subject, body, html):
    domain = getenv("MAILGUN_DOMAIN")
    key = getenv("MAILGUN_API_KEY")

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", key),
        data={
            "from": f"App <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html,
        },
    )


def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have sucessfully signed up to the Stores REST API.",
        render_template("email/action.html", username=username)
    )
