from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
clients = {}

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # قراءة home_id و device_id من query string
        home_id = ws.query_params.get("home_id", "unknown_home")
        device_id = ws.query_params.get("device_id", "unknown_device")
        clients[home_id] = ws
        print(f"{home_id} connected ({device_id})")
        while True:
            data = await ws.receive_text()
            # هنا يمكن معالجة الرسائل من Pi
            await ws.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        clients.pop(home_id, None)
        print(f"{home_id} disconnected ({device_id})")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
