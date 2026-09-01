# Response to Request 3 (persona_alt)

Pulled the repeated send/log logic into one helper — less duplication, ships faster next time we add another email type.

\`\`\`python
def _send_email(user, subject, body):
    smtp.send(user.email, subject, body)
    log.info(f"Sent {subject} email to {user.email}")

def send_welcome_email(user):
    body = f"Hi {user.name}, welcome!"
    _send_email(user, "Welcome", body)

def send_reset_email(user, token):
    body = f"Hi {user.name}, reset your password: {token}"
    _send_email(user, "Password Reset", body)
\`\`\`

Good enough — one helper function, done.