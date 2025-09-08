from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os

app = FastAPI()
clients = {}

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        # قراءة home_id و device_id من query string
        query = dict(pair.split('=') for pair in ws.query_params._dict.items())
        home_id = query.get("home_id", "unknown_home")
        device_id = query.get("device_id", "unknown_device")
        clients[home_id] = ws
        print(f"{home_id} connected ({device_id})")
        while True:
            data = await ws.receive_text()  # يمكن استقبال الرسائل
            # هنا يمكن معالجة الرسائل من Pi
    except WebSocketDisconnect:
        clients.pop(home_id, None)
        print(f"{home_id} disconnected ({device_id})")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
