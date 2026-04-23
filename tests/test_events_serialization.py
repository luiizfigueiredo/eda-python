from datetime import datetime
from decimal import Decimal

from shared.events import OrderCreatedEvent
from shared.models import Customer, OrderItem


def test_order_created_event_serialization() -> None:
    event = OrderCreatedEvent(
        order_id="order-1",
        customer=Customer(
            customer_id="cust-1",
            name="Jane Doe",
            email="jane@example.com",
            address="Rua A, 123",
        ),
        items=[
            OrderItem(
                product_id="prod-1",
                product_name="Keyboard",
                quantity=2,
                price=Decimal("50.00"),
            )
        ],
        total_amount=Decimal("100.00"),
    )

    payload = event.model_dump(mode="json")

    assert payload["event_type"] == "order.created"
    assert payload["total_amount"] == 100.0
    assert payload["items"][0]["price"] == 50.0
    # timestamp deve ser serializado como ISO string.
    datetime.fromisoformat(payload["timestamp"])
