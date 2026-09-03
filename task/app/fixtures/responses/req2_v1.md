# Response to Request 2 (persona_v1)

i'll Add input validation using simple conditional checks before writing to the database.

\`\`\`python
def create_order(customer_id, items, total):
    if not customer_id:
        raise ValueError("customer_id is required")
    if not items:
        raise ValueError("items cannot be empty")
    if not isinstance(total, (int, float)) or total <= 0:
        raise ValueError("total must be a positive number")

    db.orders.insert({
        "customer_id": customer_id,
        "items": items,
        "total": total,
    })
\`\`\`