import connexion
import yaml
import logging.config
import datetime
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def populate_stats():
    logger.info("Start Periodic Processing")

    try:
        with open(app_config['datastore']['filename'], 'r') as json_file:
            stats = json.load(json_file)
    except FileNotFoundError:
        stats = {
            "num_item_readings": 0,
            "max_item_reading": 0,
            "num_ability_readings": 0,
            "max_ability_reading": 0,
            "num_total_readings": 0,
            "last_updated": "2014-10-01 16:00:00.000000",
        }

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    time_stamp = {
        'timestamp': stats['last_updated']
    }

    try:
        ability_data = requests.get(app_config['ability']['url'], params=time_stamp)
        item_data = requests.get(app_config['item']['url'], params=time_stamp)

    except requests.RequestException as e:
        logger.error(f"Failed to retrieve data from endpoints: {str(e)}")
        return

    if ability_data.status_code == 200 and item_data.status_code == 200:
        stats['last_updated'] = current_datetime
        ability_content = ability_data.content.decode('utf-8')
        item_content = item_data.content.decode('utf-8')
        ability_json = json.loads(ability_content)
        item_json = json.loads(item_content)
        num_item_readings = len(item_json)
        max_item_reading = 0
        for reading in item_json:
            if reading['used_in_game'] > max_item_reading:
                max_item_reading = reading['used_in_game']
        num_ability_readings = len(ability_json)
        max_ability_reading = 0
        for reading in ability_json:
            if reading['used_in_game'] > max_ability_reading:
                max_ability_reading = reading['used_in_game']
        num_total_readings = num_item_readings + num_ability_readings
        stats['num_item_readings'] = num_item_readings
        stats['max_item_reading'] = max_item_reading
        stats['num_ability_readings'] = num_ability_readings
        stats['max_ability_reading'] = max_ability_reading
        stats['num_total_readings'] = num_total_readings
        with open(app_config['datastore']['filename'], 'w') as json_file:
            json.dump(stats, json_file, indent=4)

        logger.debug("Updated statistics: {}".format(stats))
    else:
        logger.error("Failed to retrieve data from endpoints")

    logger.info("Periodic Processing has ended")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
    'interval',
    seconds=app_config['scheduler']['period_sec'])
    sched.start()

def get_stats():
    logger.info('Request started.')
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return "Statistics do not exist", 404

    logger.debug(dict(data))
    logger.info("Request completed.")
    return dict(data), 200    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)