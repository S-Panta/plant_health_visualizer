# This project is a part of CEE6110 HydroInformatics
A real time plant health visualizer using MQTT protocol.

## Installation
- This project use Mosquitto broker alpine docker image. To install docker on your machine, go to https://docs.docker.com/engine/install/.
- Install the necessary library with the command "pip install -r requirements.txt" in your terminal of your IDE.
- type "docker compose up" to run the broker.

## Library
- mqtt paho client for coding publisher and subscriber. https://pypi.org/project/paho-mqtt/
- Mosquitto as a broker. https://mosquitto.org/
- Python script for data cleaup and visualizer.
- Postgresql or sqlite for storing the data.

## For collaboration
- Always make a Pull request. https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request
- Assign reviewer and then they can comment and then it will be merged.


