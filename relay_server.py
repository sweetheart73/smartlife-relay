import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    # قراءة الـ query params
    device_id = ws.query_params.get("device_id", "unknown_device")
    home_id = ws.query_params.get("home_id", "unknown_home")

    print(f"✅ Device connected: {device_id} in {home_id}")

    try:
        while True:
            data = await ws.receive_text()
            print(f"📩 Message from {device_id}@{home_id}: {data}")
            await ws.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"❌ Device {device_id} in {home_id} disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
