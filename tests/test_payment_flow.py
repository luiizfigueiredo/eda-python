from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from services.payment_service import payment
from shared.events import EventType, OrderCreatedEvent
from shared.models import Customer, OrderItem


def _build_order_event() -> OrderCreatedEvent:
    return OrderCreatedEvent(
        order_id="order-123",
        customer=Customer(
            customer_id="cust-123",
            name="John Doe",
            email="john@example.com",
            address="Main St",
        ),
        items=[
            OrderItem(
                product_id="prod-1",
                product_name="Product A",
                quantity=1,
                price=Decimal("10.50"),
            )
        ],
        total_amount=Decimal("10.50"),
    )


@pytest.mark.asyncio
async def test_handle_payment_pending_success_publishes_payment_and_shipping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    order_event = _build_order_event()
    publish_mock = AsyncMock()

    async def always_success(_: OrderCreatedEvent) -> bool:
        return True

    monkeypatch.setattr(payment, "process_payment", always_success)
    monkeypatch.setattr(payment.broker, "publish", publish_mock)

    await payment.handle_payment_pending(order_event)

    assert publish_mock.await_count == 2
    published_queues = [call.kwargs["queue"] for call in publish_mock.await_args_list]
    assert EventType.PAYMENT_PROCESSED.value in published_queues
    assert EventType.SHIPPING_PENDING.value in published_queues


@pytest.mark.asyncio
async def test_handle_payment_pending_failure_publishes_failed_event(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    order_event = _build_order_event()
    publish_mock = AsyncMock()

    async def always_fail(_: OrderCreatedEvent) -> bool:
        return False

    monkeypatch.setattr(payment, "process_payment", always_fail)
    monkeypatch.setattr(payment.broker, "publish", publish_mock)

    await payment.handle_payment_pending(order_event)

    assert publish_mock.await_count == 1
    assert publish_mock.await_args.kwargs["queue"] == EventType.PAYMENT_FAILED.value
