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
            pass  # هنا يمكنك معالجة الرسائل المرسلة من Pi
    finally:
        clients.pop(home_id, None)
        print(f"{home_id} disconnected")

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
