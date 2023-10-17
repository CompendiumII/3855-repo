import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
     app_config = yaml.safe_load(f.read())


db_connection = mysql.connector.connect(host=app_config['datastore']['hostname'],
                                   user=app_config['datastore']['user'],
                                   password=app_config['datastore']['password'],
                                   database=app_config['datastore']['db'])

db_cursor = db_connection.cursor()

db_cursor.execute('''
                  DROP TABLE ability_usage, item_usage
                  ''')

db_connection.commit()
db_connection.close()
