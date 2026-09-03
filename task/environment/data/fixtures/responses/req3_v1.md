# Response to Request 3 (persona_v1)

I'll extract the shared logic into a helper function so both email
functions stay consistent and any future changes only need to happen
in one place.

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

This removes the duplicated `smtp.send`/`log.info` calls and keeps each
function focused on just building its message body.