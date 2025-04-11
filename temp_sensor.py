import time
import json
import random
from awscrt import mqtt
from awsiot import mqtt_connection_builder
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

endpoint = config["aws_iot_temp_sensor"]["endpoint"]
client_id = config["aws_iot_temp_sensor"]["client_id"]
topic = config["aws_iot_temp_sensor"]["topic"]
cert_path = config["aws_iot_temp_sensor"]["cert_path"]
key_path = config["aws_iot_temp_sensor"]["key_path"]
root_ca = config["aws_iot_temp_sensor"]["root_ca"]

def gen_temperature():
    return round(random.uniform(15.0, 21.0), 1)

def main():
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        port=8883,
        cert_filepath=cert_path,
        pri_key_filepath=key_path,
        ca_filepath=root_ca,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=30
    )

    print(f"[Sensor] Connecting to {endpoint}...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("[Sensor] Connected!")

    for i in range(30):
        temperature = gen_temperature()
        payload = { "temperature": temperature }
        print(f"[Sensor] Publishing: {payload}")
        mqtt_connection.publish(
            topic=topic,
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