import json
from google.cloud import bigquery

credentials = 'cred.json'

project_id = "aiden-419204"
dataset_id = "SensorDataset"
table_id = "SensorData"


def insert_sensor_data(sensor_data_json):

  # Authenticate to Google Cloud (replace with your authentication method)
  #client = bigquery.Client(project=project_id, credentials=)
  client = bigquery.Client.from_service_account_json(credentials)

  # Prepare data for BigQuery
  try:
      json_data = json.loads(sensor_data_json)
      humidity = float(json_data.get('humidity'))
      temperature = float(json_data.get('temperature'))
      ppm = int(json_data.get('ppm'))
      soilHumidity = int(json_data.get('soilHumidity'))
      row = {u"humidity": humidity, u"temperature": temperature, u"ppm": ppm, u"soilHumidity": soilHumidity}
  except Exception as e:
      print(f"Error parsing JSON data: {e}")
      return

  # Insert data into BigQuery table
  table_ref = client.dataset(dataset_id).table(table_id)
  try:
      errors = client.insert_rows_json(table_ref, [row])
      if errors:
          print(f"Errors encountered during insert: {errors}")
      else:
          print(f"Data inserted successfully into BigQuery table: {table_ref}")
  except Exception as e:
      print(f"Error inserting data: {e}")
