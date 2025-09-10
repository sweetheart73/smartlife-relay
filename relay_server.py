# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()

# كل جهاز متصل نخزّنه في dict
connected_devices = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # نقبل الاتصال
    await websocket.accept()

    # قراءة الباراميترات من الـ Query String
    query_params = websocket.query_params
    device_id = query_params.get("device_id", "unknown")
    home_id = query_params.get("home_id", "default")

    device_key = f"{home_id}:{device_id}"
    connected_devices[device_key] = websocket

    print(f"✅ Device connected: {device_key}")

    try:
        while True:
            # استقبل رسالة من العميل
            data = await websocket.receive_text()
            print(f"📩 [{device_key}] {data}")

            # أرسل رد للعميل
            await websocket.send_text(f"Echo from server: {data}")

    except WebSocketDisconnect:
        print(f"❌ Device disconnected: {device_key}")
        connected_devices.pop(device_key, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080)
