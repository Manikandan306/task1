# Request 3: Refactor for Duplication

These two functions share a lot of logic. Refactor to reduce duplication:

\`\`\`python
def send_welcome_email(user):
    body = f"Hi {user.name}, welcome!"
    smtp.send(user.email, "Welcome", body)
    log.info(f"Sent welcome email to {user.email}")

def send_reset_email(user, token):
    body = f"Hi {user.name}, reset your password: {token}"
    smtp.send(user.email, "Password Reset", body)
    log.info(f"Sent reset email to {user.email}")
\`\`\`