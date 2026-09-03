# Response to Request 3 (persona_v2)

Before refactoring — should the helper function also handle the case where `smtp.send` fails, or is error handling for sending out of scope here? I'll assume it's out of scope for this refactor.

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


def test_send_welcome_email_calls_helper(monkeypatch):
    calls = []
    monkeypatch.setattr("smtp.send", lambda to, subj, body: calls.append((to, subj)))
    user = type("U", (), {"name": "Sam", "email": "sam@example.com"})()
    send_welcome_email(user)
    assert calls[0][1] == "Welcome"
\`\`\`

This extracts the shared send/log logic into `_send_email`, removing
the duplication, and includes a test confirming the welcome email
still triggers correctly.