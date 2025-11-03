from confluent_kafka import Consumer, Producer
from . import config

def _common_conf():
    conf = {
        "bootstrap.servers": config.KAFKA_BOOTSTRAP,
        "security.protocol": config.SECURITY_PROTOCOL
    }
    if config.SECURITY_PROTOCOL.upper() == "SASL_SSL":
        conf.update({
            "sasl.mechanism": config.SASL_MECHANISM or "PLAIN",
            "sasl.username": config.SASL_USERNAME,
            "sasl.password": config.SASL_PASSWORD,
        })
    return conf

def make_consumer(group_id="genai-app"):
    conf = _common_conf()
    conf.update({
        "group.id":"%s" % group_id,
        "auto.offset.reset":"earliest",
        "enable.auto.commit": True
    })
    c = Consumer(conf)
    c.subscribe([config.INPUT_TOPIC])
    return c

def make_producer():
    return Producer(_common_conf())

def produce_json(p, topic, obj):
    import json
    p.produce(topic, json.dumps(obj).encode("utf-8"))
    p.flush()
