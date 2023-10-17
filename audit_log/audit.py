import connexion
import logging.config
import yaml
import json
from pykafka import KafkaClient

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_item_stats(index):
    kafka_server = app_config['events']['hostname']
    kafka_port = app_config['events']['port']
    client = KafkaClient(hosts=f"{kafka_server}:{kafka_port}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    
    logger.info("Retrieving item statistic at index %d" % index)

    current_index = 0

    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)

            if msg['type'] == 'item':
                if current_index == index:
                    return { "message": msg }, 200
                else:
                    current_index += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find item statistic at index %d" % index)
    return { "message": "Not found" }, 404

def get_ability_stats(index):
    kafka_server = app_config['events']['hostname']
    kafka_port = app_config['events']['port']
    client = KafkaClient(hosts=f"{kafka_server}:{kafka_port}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
                                         consumer_timeout_ms=1000)
    
    logger.info("Retrieving ability statistic at index %d" % index)
    current_index = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'ability':
                if current_index == index:
                    return {'message': msg}, 200
                else:
                    current_index += 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find ability statistic at index %d" % index)
    return { "message": "Not found" }, 404

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8110, use_reloader=False)