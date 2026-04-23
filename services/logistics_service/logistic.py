if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )

import asyncio
from datetime import datetime
from random import random

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from shared.envs import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER
from shared.events import (
    EventType,
    OrderShippedEvent,
    PaymentProcessedEvent,
    ShippingFailedEvent,
)

broker = RabbitBroker(
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
)
app = FastStream(broker)


async def process_shipping_success() -> bool:
    """Simula o processamento de envio com chance de falha."""
    await asyncio.sleep(1)

    success_rate = 0.2
    return random() < success_rate


@broker.subscriber(EventType.SHIPPING_FAILED.value)
async def shipping_failed(shipping_failed_event: ShippingFailedEvent):
    """Log de eventos de envio com falha."""
    print(
        f"Shipping failed for order {shipping_failed_event.order_id} reason: {shipping_failed_event.reason}"
    )


@broker.subscriber(EventType.ORDER_SHIPPED.value)
async def shipping_success(shipping_success_event: OrderShippedEvent):
    """Log do evento final canônico de envio com sucesso."""
    print(
        f"Shipping success for order {shipping_success_event.order_id} by {shipping_success_event.tracking_code}"
    )


@broker.subscriber(EventType.SHIPPING_PENDING.value)
async def process_shipping(order_event: PaymentProcessedEvent):
    """Processa envio a partir de pagamento aprovado."""
    print(f"Processing shipping for order {order_event.order_id}")
    success = await process_shipping_success()

    if success:
        shipped_event = OrderShippedEvent(
            order_id=order_event.order_id,
            tracking_code="trucker",
            estimated_delivery=datetime.now(),
        )
        await broker.publish(shipped_event, queue=EventType.ORDER_SHIPPED.value)
    else:
        failed_shipping = ShippingFailedEvent(
            order_id=order_event.order_id,
            reason="Failed to ship",
        )

        await broker.publish(failed_shipping, queue=EventType.SHIPPING_FAILED.value)


if __name__ == "__main__":
    asyncio.run(app.run())
