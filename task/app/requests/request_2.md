# Request 2: Validate Input

Add input validation to this function before it writes to the database:

\`\`\`python
def create_order(customer_id, items, total):
    db.orders.insert({
        "customer_id": customer_id,
        "items": items,
        "total": total,
    })
\`\`\`