import asyncio, json
subscribers: set[asyncio.Queue] = set()

async def publish(payload: dict):
    for q in list(subscribers):
        await q.put(payload)

async def event_generator():
    q: asyncio.Queue = asyncio.Queue()
    subscribers.add(q)
    try:
        while True:
            payload = await q.get()
            yield f"data: {json.dumps(payload, default=str, ensure_ascii=False)}\n\n"
    finally:
        subscribers.discard(q)
