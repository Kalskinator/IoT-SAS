# DA643E: Software Architecture and Security for IoT
## Assignment 1: Automated Temperature Adjustment in Smart Offices

### 1. Temperature Sensor (temp_sensor.py)
Simulates a temperature sensor device that:
- Connects to AWS IoT Core using MQTT protocol
- Generates temperature readings between 15.0°C and 21.0°C
```python
def gen_temperature():
    return round(random.uniform(15.0, 21.0), 1)
```
- Publishes temperature readings every 2 seconds for 30 iterations
```python
from awscrt import mqtt
payload = { "temperature": temperature }
mqtt_connection.publish(
    topic=topic,
    payload=json.dumps(payload),
    qos=mqtt.QoS.AT_LEAST_ONCE
)
```

### 2. Thermostat Controller (thermostat.py)
Smart thermostat that:
- Connects to AWS IoT Core using MQTT protocol
- Subscribes to MQTT topic
```python
from awscrt import mqtt
subscribe_future, packet_id = mqtt_client.subscribe(
    topic=TOPIC, 
    qos=mqtt.QoS.AT_LEAST_ONCE, 
    callback=on_message_received
)
```
- Implements a message callback handler
```python
def on_message_received(topic, payload, **kwargs):
    print(f"Received message from topic '{topic}': {payload.decode('utf-8')}")
```
- Stays connected and listens for incoming messages, can be terminated with keyboard interrupt

### 3. Lambda Function (lambda_function.py)
AWS Lambda function for decision-making:
- Receives temperature readings as events from AWS IoT Core and Maintains a rolling window of the last 3 temperature readings and calculates average
```python
temperature = event.get("temperature")
last_3_readings = deque(maxlen=3)
last_3_readings.append(temperature)
avg_temp = sum(last_3_readings) / len(last_3_readings)
```
- Implements the control logic which publishes control commands to thermostat:
```python
response = iot_client.publish(
    topic='smart_office_3/thermostat',
    qos=1,
    payload=payload
)
```
  - If average temperature < 18°C: Sends "activate_heater" command to thermostat
```python
payload = json.dumps({"action": f"activate_heater"})
```
  <!-- - If average temperature ≥ 18°C: Sends "no_need_to_activate_heater" message
```python
payload = json.dumps({"action": f"no_need_to_activate_heate"})
``` -->
### Data Flow
1. Temperature sensor publishes readings to AWS IoT Core
2. AWS IoT Core triggers the Lambda function with the temperature data
3. Lambda function processes the data and makes heating decisions
4. Lambda function publishes control commands back to AWS IoT Core
5. Thermostat receives and processes the control commands

### Configuration
All device-specific settings (endpoints, certificates, client IDs, topics) are managed through a hidden config.ini file
