if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

import asyncio
import random
from uuid import uuid4

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.envs import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS
from shared.events import (
    EventType,
    OrderCreatedEvent,
    PaymentFailedEvent,
    PaymentProcessedEvent,
)

broker = RabbitBroker(
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
)
app = FastStream(broker)


async def process_payment(order_event: OrderCreatedEvent) -> bool:
    """Simula o processamento de pagamento com chance de falha."""
    await asyncio.sleep(1)

    success_rate = 0.2
    return random.random() < success_rate

@broker.subscriber(EventType.PAYMENT_PROCESSED.value)
async def paymente_processed(payment_processed_event: PaymentProcessedEvent):
    """Processa o pagamento quando um pedido é criado."""
    print(
        f"Payment processed successfully: {payment_processed_event.payment_id} for order {payment_processed_event.order_id}"
    )

@broker.subscriber(EventType.PAYMENT_FAILED.value)
async def payment_failed(payment_failed_event: PaymentFailedEvent):
    """Processa o pagamento quando um pedido é criado."""
    print(
        f"Payment failed for order {payment_failed_event.order_id} reason: {payment_failed_event.reason}"
    )


@broker.subscriber(EventType.PAYMENT_PENDING.value)
async def handle_payment_pending(order_event: OrderCreatedEvent):
    """Processa o pagamento quando um pedido é criado."""
    print(f"Received PaymentPending event: {order_event.order_id}")
    print(f"Amount to process: ${order_event.total_amount}")

    payment_success = await process_payment(order_event)

    if payment_success:
        payment_id = str(uuid4())
        payment_event = PaymentProcessedEvent(
            order_id=order_event.order_id,
            payment_id=payment_id,
            amount=order_event.total_amount,
            status="approved",
        )
        await broker.publish(payment_event, queue=EventType.PAYMENT_PROCESSED.value)
    else:
        payment_failed_event = PaymentFailedEvent(
            order_id=order_event.order_id,
            reason="Insufficient funds or payment gateway error",
        )
        await broker.publish(
            payment_failed_event, queue=EventType.PAYMENT_FAILED.value
        )

if __name__ == "__main__":
    asyncio.run(app.run())
