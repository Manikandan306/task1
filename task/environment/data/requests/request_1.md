# Request 1: Retry Logic

Add retry logic to this function, which calls an unreliable external API:

\`\`\`python
def fetch_user_data(user_id):
    response = api_client.get(f"/users/{user_id}")
    return response.json()
\`\`\`

Make it resilient to transient failures.