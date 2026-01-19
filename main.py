from faststream import FastStream
from faststream.redis import RedisBroker
from shared.envs import REDIS_HOST, REDIS_PORT

broker = RedisBroker(f"redis://{REDIS_HOST}:{REDIS_PORT}")

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
    app()
