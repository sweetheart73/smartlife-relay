import asyncio
import websockets

clients = {}

async def handler(ws, path):
    query = dict(pair.split('=') for pair in path[2:].split('&'))
    home_id = query.get("home_id")
    clients[home_id] = ws
    print(f"{home_id} connected")
    try:
        async for message in ws:
            pass  # هنا يمكن معالجة الرسائل المرسلة من Pi
    finally:
        clients.pop(home_id, None)
        print(f"{home_id} disconnected")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Relay Server is running on ws://0.0.0.0:8765")
        await asyncio.Future()  # يبقي السيرفر يعمل إلى ما لا نهاية

if __name__ == "__main__":
    asyncio.run(main())
