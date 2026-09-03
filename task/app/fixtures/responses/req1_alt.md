# Response to Request 1 (persona_alt)

I'll add retry logic using a simple loop with exponential backoff.

\`\`\`python
import time

def fetch_user_data(user_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = api_client.get(f"/users/{user_id}")
            return response.json()
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
\`\`\`

This retries up to 3 times with exponential backoff, good enough to ship.