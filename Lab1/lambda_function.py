import json
import boto3
from collections import deque

last_3_readings = deque(maxlen=3)
iot_client = boto3.client('iot-data', region_name='eu-north-1')

def lambda_handler(event, context):
    print(f"Received event: {event}")
    try:
        temperature = event.get("temperature")
        if temperature is None:
            return {"status": "no temperature in message"}

        last_3_readings.append(temperature)
        print(f"Last 3 temperatures: {list(last_3_readings)}")
        
        avg_temp = sum(last_3_readings) / len(last_3_readings)
        print(f"Average temperature: {avg_temp}")
        if avg_temp < 18:
            response = iot_client.publish(
                topic='smart_office_3/thermostat',
                qos=1,
                payload=json.dumps({"action": f"activate_heater because avg temp is {avg_temp}"})
            )
            print("Published 'activate_heater' to thermostat topic")
        else:
            response = iot_client.publish(
                topic='smart_office_3/thermostat',
                qos=1,
                payload=json.dumps({"action": f"no_need_to_activate_heater becasue avg temp is {avg_temp}"})
            )
            print("Published 'nothing' to thermostat topic")
        return {"status": "success", "avg_temp": avg_temp}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}
