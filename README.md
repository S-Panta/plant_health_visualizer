# This project is a part of CEE6110 HydroInformatics
A real time plant health visualizer using MQTT protocol.

## Installation
- This project use Mosquitto broker alpine docker image. To install docker on your machine, go to https://docs.docker.com/engine/install/.
- Install the necessary library with the command "pip install -r requirements.txt" in your terminal of your IDE.
- type "docker compose up" to run Mosquitto broker.
- You should have sqlite database file at the root of your project folder. Make sure the file exists 
- Run publisher.py and subscriber.py.
```python
    python mqtt/publisher.py
    python mqtt/subscriber.py
```
- Download blank_odm.sqlite from [source] and place it in the project root

## Library
- mqtt paho client for coding publisher and subscriber. https://pypi.org/project/paho-mqtt/
- Mosquitto as a broker. https://mosquitto.org/
- Python script for data cleaup and visualizer.
- Postgresql or sqlite for storing the data.


