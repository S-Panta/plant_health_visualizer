import json
import paho.mqtt.client as mqtt
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from database.connection import DatabaseManager

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "campbell/NDVI_data"

consumer = DatabaseManager()


def prepare_ndvi_data(payload):
    local_dt = datetime.fromisoformat(payload["LocalDateTime"])
    utc_dt = local_dt + timedelta(hours=7)
    return {
        "DataValue": payload["NDVI_avg"],
        "ValueAccuracy": None,
        "LocalDateTime": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "UTCOffset": -7.0,
        "DateTimeUTC": utc_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "SiteID": 1,
        "VariableID": 1,
        "OffsetValue": None,
        "OffsetTypeID": None,
        "CensorCode": "nc",
        "MethodID": 0,
        "SourceID": 1,
        "SampleID": None,
        "DerivedFromID": None,
        "QualityControlLevelID": 0,
    }


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
        consumer.insert_row("datavalues", prepare_ndvi_data(data))
        consumer.commit_to_database()
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
