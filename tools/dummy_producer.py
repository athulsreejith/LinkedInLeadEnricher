import json
import time
import os
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

BOOT = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("INPUT_TOPIC", "salesforce_myleads")

conf = {
    "bootstrap.servers": BOOT,
    "security.protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
}

sasl_mechanism = os.getenv("KAFKA_SASL_MECHANISM")
if sasl_mechanism and sasl_mechanism.strip():
    conf["sasl.mechanisms"] = sasl_mechanism.strip()
    sasl_username = os.getenv("KAFKA_SASL_USERNAME", "").strip()
    sasl_password = os.getenv("KAFKA_SASL_PASSWORD", "").strip()
    if sasl_username:
        conf["sasl.username"] = sasl_username
    if sasl_password:
        conf["sasl.password"] = sasl_password

p = Producer(conf)

samples = [
    {"full_name": "Edwin Francis", "company": "SureFlow", "email": "edwinfrancis786@gmail.com"},
    {"full_name": "Carsten Mützlitz", "company": "Confluent", "email": "carsten@example.com"}
]

for s in samples:
    p.produce(TOPIC, json.dumps(s).encode("utf-8"))
    p.flush()
    print("Sent:", s)
    time.sleep(1)
