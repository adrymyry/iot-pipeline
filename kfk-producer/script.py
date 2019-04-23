import time
import datetime
import json

import paho.mqtt.client as mqtt
from kafka import KafkaProducer

time.sleep(30)
producer = KafkaProducer(bootstrap_servers="kafka:9092", \
    value_serializer=lambda v: json.dumps(v).encode("utf-8"))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("umu/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    topic = msg.topic
    measure_type = topic.split("/")[-1]
    location = topic.replace("/"+measure_type, "")

    json_kafka = {
        "measure": measure_type,
        "location": location,
        "date": datetime.datetime.now().isoformat(),
        "value": str(msg.payload)
    }

    print(json_kafka)
    producer.send("sensor_data", json_kafka)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-brocker", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()