from serial import Serial
import json

import pubsub
import bigquery_connection
from db_connection import DBConnection

def send_message(data):
    pubsub.publish_data('SensorData', data)
    # uncomment to upload data directly from pi
    # bigquery_connection.insert_sensor_data(data)


def main():
    arduino = Serial('/dev/ttyACM0', 9600)
    
    # first line is garbage
    arduino.readline()

    while True:
        line = arduino.readline().decode('utf-8').strip()

        values = line.split()

        dict = {
            'ppm': values[0],
            'humidity': values[1],
            'temperature': values[2],
            'soilHumidity': values[3],
        }

        send_message(json.dumps(dict))


if __name__ == "__main__":
    main()
