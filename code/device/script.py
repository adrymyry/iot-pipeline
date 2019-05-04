import paho.mqtt.client as mqtt
import time
import random
import os
# import Adafruit_DHT

# sensor = Adafruit_DHT.DHT11
# pin = 23

location = os.environ["LOCATION"]
location = location if location else "fac_info/lab"

time.sleep(5)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("mqtt-brocker")
client.loop_start()

while True:
    #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    temperature = (25-20) * random.random() + 20
    client.publish(location+"/temperature", temperature)
    time.sleep(5)