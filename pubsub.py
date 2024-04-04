from google.cloud import pubsub_v1
import json

project_id = 'aiden-419204'
credentials = 'cred.json'

def create_topic(topic_name):
    publisher = pubsub_v1.PublisherClient.from_service_account_json(credentials)
    topic_path = publisher.topic_path(project_id, topic_name)
    topic = publisher.create_topic(request={"name": topic_path})
    print(f"Created topic: {topic.name}")

def delete_topic(topic_name):
    publisher = pubsub_v1.PublisherClient.from_service_account_json(credentials)
    topic_path = publisher.topic_path(project_id, topic_name)
    publisher.delete_topic(request={"topic": topic_path})
    print(f"Topic deleted: {topic_path}")

def publish_data(topic_name, data):
    publisher = pubsub_v1.PublisherClient.from_service_account_json(credentials)
    topic_path = publisher.topic_path(project_id, topic_name)
    future = publisher.publish(topic_path, data.encode("utf-8"))
    print(f"Published message ID: {future.result()}")

def publish_json_data(topic_name, data_path):

    with open(data_path) as f:
        data = json.load(f)

    publisher = pubsub_v1.PublisherClient.from_service_account_json(credentials)
    topic_path = publisher.topic_path(project_id, topic_name)
    stringified_data = json.dumps(data).encode("utf-8")
    future = publisher.publish(topic_path, stringified_data)
    print(f"Published message ID: {future.result()}")

# ------------------------------------ playground ----------------------------------------------------

def main():
    print('PubSub playground activated.')
    # create_topic('SensorData2')
        
    # delete_topic('SensorData')

    # publish_data('SensorData2', 'Hello, World!')
    # publish_json_data('SensorData', 'data/json/sensor.json')
    
if __name__ == "__main__":
    main()