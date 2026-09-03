# Response to Request 2 (persona_v2)

Before I add validation — should `items` allow an empty list if the order has no line items yet, or should it always require at least one item? I'll assume at least one item is required.

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


def test_create_order_rejects_missing_customer_id():
    try:
        create_order(None, ["item1"], 10)
        assert False, "expected ValueError"
    except ValueError:
        assert True
\`\`\`

This validates all three inputs up front and raises a clear error for
each bad case, with a test confirming the missing-`customer_id` case
is caught.