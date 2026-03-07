if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))) 

import asyncio
import random
from decimal import Decimal
from uuid import uuid4

from faststream import FastStream
from faststream.redis import RedisBroker

from shared.envs import REDIS_HOST, REDIS_PORT
from shared.events import OrderCreatedEvent, EventType
from shared.models import Customer, OrderItem

broker = RedisBroker(f"redis://{REDIS_HOST}:{REDIS_PORT}")
app = FastStream(broker)

@broker.subscriber(EventType.ORDER_CREATED.value)
async def next_handler(body):
    await broker.publish(body, channel=EventType.PAYMENT_PENDING.value)

async def create_mock_order() -> OrderCreatedEvent:
    customer = Customer(
        customer_id=str(uuid4()),
        name="John Doe",
        email="john@example.com",
        address="123 Main St",
    )
    
    items = [
        OrderItem(
            product_id=str(uuid4()),
            product_name="Product A",
            quantity=random.randint(1, 4),
            price=Decimal("10.50"),
        ),
        OrderItem(
            product_id=str(uuid4()),
            product_name="Product B",
            quantity=random.randint(1, 2),
            price=Decimal("20.00"),
        )
    ]
    
    total = sum(i.price * i.quantity for i in items)
    
    return OrderCreatedEvent(
        order_id=str(uuid4()),
        customer=customer,
        items=items,
        total_amount=total
    )

@app.after_startup
async def publish_orders():
    await asyncio.sleep(2)
    
    while True:
        order_event = await create_mock_order()
        await broker.publish(order_event, channel=EventType.ORDER_CREATED.value)
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(app.run())
