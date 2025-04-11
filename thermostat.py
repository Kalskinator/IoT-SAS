from awscrt import mqtt
from awsiot import mqtt_connection_builder
import json
import time
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

ENDPOINT = config['aws_iot_thermostat']['endpoint']
CLIENT_ID = config['aws_iot_thermostat']['client_id']
TOPIC = config['aws_iot_thermostat']['topic']
ROOT_CA = config['aws_iot_thermostat']['root_ca']
KEY_PATH = config['aws_iot_thermostat']['key_path']
CERT_PATH = config['aws_iot_thermostat']['cert_path']

# Callback function for received messages
def on_message_received(topic, payload, **kwargs):
    print(f"Received message from topic '{topic}': {payload.decode('utf-8')}")


def main():
    mqtt_client = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_PATH,
        pri_key_filepath=KEY_PATH,
        ca_filepath=ROOT_CA,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30
    )

    print(f"[Thermostat] Connecting to {ENDPOINT}...")
    connect_future = mqtt_client.connect()
    connect_future.result()
    print("[Thermostat] Connected!")

    print("Subscribing to topic '{}'...".format(TOPIC))
    subscribe_future, packet_id = mqtt_client.subscribe(
        topic=TOPIC, 
        qos=mqtt.QoS.AT_LEAST_ONCE, 
        callback=on_message_received
    )

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result["qos"])))

    try:
        while True:
            pass 
    except KeyboardInterrupt:
        print("Disconnecting...")
        disconnect_future = mqtt_client.disconnect()
        disconnect_future.result()
        print("Disconnected!")


if __name__ == "__main__":
    main()