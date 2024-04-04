import functions_framework
import json
import base64
import datetime
from google.cloud import bigquery

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def handle_pubsub(cloud_event):

    print(cloud_event)

    sensor_data = base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')

    client = bigquery.Client()
    project_id = "aiden-419204"
    dataset_id = "SensorDataset"
    table_id = "SensorData"

    try:
        json_data = json.loads(sensor_data)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        humidity = float(json_data.get('humidity'))
        temperature = float(json_data.get('temperature'))
        ppm = int(json_data.get('ppm'))
        soilHumidity = int(json_data.get('soilHumidity'))
        row = {u"timestamp": timestamp, u"humidity": humidity, u"temperature": temperature, u"ppm": ppm, u"soilHumidity": soilHumidity}
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return

    table_ref = client.dataset(dataset_id).table(table_id)

    try:
        errors = client.insert_rows_json(table_ref, [row])
        if errors:
            print(f"Errors encountered during insert: {errors}")
        else:
            print(f"Data inserted successfully into BigQuery table: {table_ref}")
    except Exception as e:
        print(f"Error inserting data: {e}")