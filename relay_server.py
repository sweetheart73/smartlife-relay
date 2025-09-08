import asyncio
import websockets
import os

clients = {}

async def handler(ws, path):
    # قراءة home_id و device_id من query string
    query = dict(pair.split('=') for pair in path[2:].split('&'))
    home_id = query.get("home_id")
    device_id = query.get("device_id")
    clients[home_id] = ws
    print(f"{home_id} connected ({device_id})")
    try:
        async for message in ws:
            pass  # هنا يمكن معالجة الرسائل القادمة من Pi
    finally:
        clients.pop(home_id, None)
        print(f"{home_id} disconnected ({device_id})")

async def main():
    PORT = int(os.environ.get("PORT", 8765))  # Railway يعين PORT تلقائيًا
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Relay Server is running on port {PORT}")
        await asyncio.Future()  # يبقي السيرفر يعمل إلى ما لا نهاية

if __name__ == "__main__":
    asyncio.run(main())
