import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import uuid
import datetime
import json
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

headers = {"Content-Type": 'application/json; charset=utf-8'}


def record_ability_usage(body):
    body["trace_id"] = str(uuid.uuid4())
    logger.info(f"Event received 'RECORD_ABILITY_USAGE' with trace id {body['trace_id']}")
    kafka_server = app_config['events']['hostname']
    kafka_port = app_config['events']['port']
    client = KafkaClient(hosts=f"{kafka_server}:{kafka_port}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "ability",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info(f"Returned event 'RECORD_ABILITY_USAGE' response(Id: {body['trace_id']})")
    return NoContent, 201

def record_item_usage(body):
    body["trace_id"] = str(uuid.uuid4())
    logger.info(f"Event received 'RECORD_ITEM_USAGE' with trace id {body['trace_id']}")
    kafka_server = app_config['events']['hostname']
    kafka_port = app_config['events']['port']
    client = KafkaClient(hosts=f"{kafka_server}:{kafka_port}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = { "type": "item",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info(f"Returned event 'RECORD_ITEM_USAGE' response(Id: {body['trace_id']})")
    return NoContent, 201
 

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)