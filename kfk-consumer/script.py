import time
import json

from kafka import KafkaConsumer
from influxdb import InfluxDBClient

time.sleep(30)
consumer = KafkaConsumer('sensor_data', \
    bootstrap_servers='kafka:9092', \
    value_deserializer=lambda m: json.loads(m.decode('utf-8')))
db_client = InfluxDBClient('influxdb', 8086, database='iotdata')


for message in consumer:
    data = message.value
    print(data)

    json_influx = [
        {
            "measurement": data['measure'],
            "tags": {
                "location": data['location'],
            },
            "time": data['date'],
            "fields": {
                "value": float(data['value'][2:-1])
            }
        }
    ]

    print(json_influx)

    db_client.write_points(json_influx)
