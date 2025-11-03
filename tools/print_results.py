import json
from confluent_kafka import Consumer
from dotenv import load_dotenv; load_dotenv()
import os

BOOT = os.getenv("KAFKA_BOOTSTRAP","localhost:29092")
TOPIC = os.getenv("OUTPUT_TOPIC","salesforce_icebreakers")

c = Consumer({
    "bootstrap.servers": BOOT,
    "group.id":"printer",
    "auto.offset.reset":"earliest"
})
c.subscribe([TOPIC])
print("Consuming results from", TOPIC)
while True:
    msg = c.poll(1.0)
    if not msg: continue
    if msg.error(): print("Err:", msg.error()); continue
    print(json.loads(msg.value().decode()))
