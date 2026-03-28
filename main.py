import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from shared.envs import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS

broker = RabbitBroker(
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
)

app = FastStream(broker)

@broker.subscriber("test_middle")
async def handler():
    await broker.publish("recebido pelo test_middle", "test_official")

@broker.subscriber("test_official")
async def next_handler(body):
    print(body)

@app.after_startup
async def startup():
    await broker.publish("", "test_middle")

if __name__ == "__main__":
    asyncio.run(app.run())
