import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from record_ability import RecordAbility
from record_item import RecordItem
import yaml
import logging.config
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

with open('app_conf.yml', 'r') as f:
     app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine(f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def get_item_usage(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")


    readings = session.query(RecordItem).filter(RecordItem.date_created >= timestamp_datetime)

    results_list = []
    
    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for item usages after %s returns %d results" %
                (timestamp, len(results_list)))

    return results_list, 200



def get_ability_usage(timestamp):
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")


    readings = session.query(RecordAbility).filter(RecordAbility.date_created >= timestamp_datetime).all()

    results_list = []

    if readings is not None:
        for reading in readings:
            results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for ability usages after %s returns %d results" % (timestamp, len(results_list)))

    return results_list, 200

def process_messages():
    kafka_server = app_config['events']['hostname']
    kafka_port = app_config['events']['port']
    client = KafkaClient(hosts=f"{kafka_server}:{kafka_port}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST)
    

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        
        payload = msg["payload"]

        session = DB_SESSION()

        if msg["type"] == "ability":
            logger.info("Received request with ability data: %s, type: %s" % (msg["payload"], type(msg["payload"])))
            ability_usage = RecordAbility(
                            payload['steam_id'],
                            payload['match_id'],
                            payload['game_version'],
                            payload['region'],
                            payload['hero_id'],
                            payload['hero_name'],
                            payload['ability_id'],
                            payload['ability_name'],
                            payload['ability_level'],
                            payload['used_in_game'],
                            payload['trace_id'])
            session.add(ability_usage)
            session.commit()
            session.close()
        elif msg["type"] == "item":
            logger.info("Received request with item data: %s, type: %s" % (msg["payload"], type(msg["payload"])))
            session = DB_SESSION()
            item_usage = RecordItem(
                            payload['steam_id'],
                            payload['match_id'],
                            payload['game_version'],
                            payload['region'],
                            payload['item_id'],
                            payload['item_name'],
                            payload['item_type'],
                            payload['item_cost'],
                            payload['obtain_status'],
                            payload['used_in_game'],
                            payload['trace_id'])
            session.add(item_usage)
            session.commit()
            session.close()
        logger.info("Successful commit!")
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    logger.info("Connecting to DB. Hostname: %s, Port: %d" % (app_config['datastore']['hostname'], app_config['datastore']['port']))
    app.run(port=8090)