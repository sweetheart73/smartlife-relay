from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    # قبول الاتصال
    await ws.accept()

    # قراءة الـ query params من URL
    device_id = ws.query_params.get("device_id")
    home_id = ws.query_params.get("home_id")

    print(f"New device connected: {device_id} in {home_id}")

    try:
        while True:
            data = await ws.receive_text()
            print(f"Message from {device_id}: {data}")
            await ws.send_text(f"Echo: {data}")
    except Exception as e:
        print(f"Connection with {device_id} lost:", e)
