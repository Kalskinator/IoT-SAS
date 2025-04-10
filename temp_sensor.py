import time
import json
import random
from awscrt import mqtt
from awsiot import mqtt_connection_builder

ENDPOINT = "a1y7d41s0oj85v-ats.iot.eu-north-1.amazonaws.com"  
CLIENT_ID = "TemperatureSensor"
TOPIC = "smart_office_3/temperature"
CERT_PATH = "certs/device.pem.crt"
KEY_PATH = "certs/private.pem.key"
ROOT_CA = "certs/AmazonRootCA1.pem"

def gen_temperature():
    return round(random.uniform(15.0, 23.0), 1)

def main():
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        port=8883,
        cert_filepath=CERT_PATH,
        pri_key_filepath=KEY_PATH,
        ca_filepath=ROOT_CA,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30
    )

    print(f"[Sensor] Connecting to {ENDPOINT}...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("[Sensor] Connected!")

    for i in range(10):
        temperature = gen_temperature()

        payload = {
            "temperature": temperature,
        }

        print(f"[Sensor] Publishing: {payload}")
        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        time.sleep(2)  

    print("[Sensor] Done sending data. Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("[Sensor] Disconnected.")

if __name__ == "__main__":
    main()