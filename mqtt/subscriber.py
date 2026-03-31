import json
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "ndvi/sensor/data"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Subscriber is connected to broker")
        client.subscribe(TOPIC, qos=1)
    else:
        print("Connection failed:", reason_code)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(data)
    except Exception as e:
        print("Error:", e)


client = mqtt.Client(
    client_id="ndvi_subscriber", callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT)
client.loop_forever()
