from unittest.mock import AsyncMock
from decimal import Decimal

import pytest

from services.logistics_service import logistic
from shared.events import EventType, PaymentProcessedEvent


def _build_payment_processed_event() -> PaymentProcessedEvent:
    return PaymentProcessedEvent(
        order_id="order-123",
        payment_id="pay-123",
        amount=Decimal("10.50"),
        status="approved",
    )


@pytest.mark.asyncio
async def test_process_shipping_success_publishes_order_shipped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    publish_mock = AsyncMock()

    async def always_success() -> bool:
        return True

    monkeypatch.setattr(logistic, "process_shipping_success", always_success)
    monkeypatch.setattr(logistic.broker, "publish", publish_mock)

    await logistic.process_shipping(_build_payment_processed_event())

    assert publish_mock.await_count == 1
    assert publish_mock.await_args.kwargs["queue"] == EventType.ORDER_SHIPPED.value


@pytest.mark.asyncio
async def test_process_shipping_failure_publishes_shipping_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    publish_mock = AsyncMock()

    async def always_fail() -> bool:
        return False

    monkeypatch.setattr(logistic, "process_shipping_success", always_fail)
    monkeypatch.setattr(logistic.broker, "publish", publish_mock)

    await logistic.process_shipping(_build_payment_processed_event())

    assert publish_mock.await_count == 1
    assert publish_mock.await_args.kwargs["queue"] == EventType.SHIPPING_FAILED.value
