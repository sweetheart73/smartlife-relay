# server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import paho.mqtt.client as mqtt

app = FastAPI()

# ----------------------------
# MQTT إعداد
# ----------------------------
MQTT_BROKER = "broker.hivemq.com"  # يمكن تغييره لسيرفرك
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "smartlifehub/"

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("✅ MQTT Connected with result code", rc)
    client.subscribe(MQTT_TOPIC_PREFIX + "#")

def on_message(client, userdata, msg):
    print(f"📡 MQTT Received: {msg.topic} -> {msg.payload.decode()}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

# ----------------------------
# WebSocket Relay
# ----------------------------
connected_devices = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    query_params = websocket.query_params
    device_id = query_params.get("device_id", "unknown")
    home_id = query_params.get("home_id", "default")

    device_key = f"{home_id}:{device_id}"
    connected_devices[device_key] = websocket

    print(f"✅ Device connected: {device_key}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 [{device_key}] {data}")

            # إذا أرسل العميل "ON" أو "OFF" نبعث عبر MQTT
            if data.lower() in ["on", "off"]:
                mqtt_client.publish(MQTT_TOPIC_PREFIX + device_key, data)
                await websocket.send_text(f"MQTT sent: {data}")
            else:
                await websocket.send_text(f"Echo from server: {data}")

    except WebSocketDisconnect:
        print(f"❌ Device disconnected: {device_key}")
        connected_devices.pop(device_key, None)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080)
