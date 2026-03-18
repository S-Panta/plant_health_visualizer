import time
import json
import sys
import os
import paho.mqtt.client as mqtt

# this line is necessary for the relative imports
# For more detail on how python imports the model, see https://docs.python.org/3/library/sys_path_init.html
# this add to the list from sys.path that is used for searching of module
# or export the current path of project(root of the project) to PYTHONPATH and this code can be removed.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# replace this with the function that is used to generate the ndvi sensor data
# the function will generate a dataframe like this
#  df = pd.DataFrame({
#         'LocalDateTime': timestamps,
#         'NDVI_avg': NDVI_avg,
#         'LowWatts_m2_avg': LowWatts_m2_avg,
#         'HighWatts_m2_avg': HighWatts_m2_avg,
#         'Battery_V_avg': Battery_V_avg,
#         'TS_min': TS_min
#     })
from data_source.script import generate_ndvi_data

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "ndvi/sensor/data"
CLIENT_ID = "ndvi_publisher"


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Publisher is connected to broker")
    else:
        print(f"Connect failed: {reason_code}")


def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"Disconnected: {reason_code}")


client = mqtt.Client(
    client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

try:
    ndvi_data = generate_ndvi_data()
    for _, row in ndvi_data.iterrows():
        record = row.to_dict()
        record["LocalDateTime"] = record["LocalDateTime"].isoformat()
        payload = json.dumps(record)
        client.publish(TOPIC, payload, qos=1)
        print(record)
        # change this to the frequency of data published by datalogger
        time.sleep(5)

finally:
    client.loop_stop()
    client.disconnect()
