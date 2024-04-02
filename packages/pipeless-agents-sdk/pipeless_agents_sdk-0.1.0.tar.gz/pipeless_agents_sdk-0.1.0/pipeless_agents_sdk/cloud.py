from json import loads
import os
import atexit
from kafka import KafkaConsumer

USERNAME = os.environ.get('SDK_USERNAME')
if USERNAME is None:
    raise ValueError("USERNAME env var must be set")

PASSWORD = os.environ.get('SDK_PASSWORD')
if PASSWORD is None:
    raise ValueError("PASSWORD env var must be set")

PROJECT_ID = os.environ.get('PROJECT_ID')
if PROJECT_ID is None:
    raise ValueError("PROJECT_ID env var must be set")

SERVER = os.environ.get('SERVER')
if SERVER is None:
    raise ValueError("SERVER env var must be set")

data_stream = KafkaConsumer(
    PROJECT_ID,
    bootstrap_servers=SERVER,
    sasl_mechanism='SCRAM-SHA-256',
    security_protocol='SASL_SSL',
    sasl_plain_username=USERNAME,
    sasl_plain_password=PASSWORD,
    group_id=PROJECT_ID, # avoid to consume messages twice on restarts
    auto_offset_reset='earliest',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

def cleanup():
    data_stream.close()

atexit.register(cleanup)
