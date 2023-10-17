import mysql
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
          CREATE TABLE item_usage
          (id INT NOT NULL AUTO_INCREMENT,
           date_created VARCHAR(100) NOT NULL,
           steam_id BIGINT NOT NULL,
           match_id BIGINT NOT NULL,
           game_version VARCHAR(100) NOT NULL,
           region VARCHAR(100) NOT NULL,
           item_id INTEGER NOT NULL,
           item_name VARCHAR(100) NOT NULL,
           item_type VARCHAR(100) NOT NULL,
           item_cost INTEGER NOT NULL,
           obtain_status VARCHAR(100) NOT NULL,
           used_in_game INTEGER NOT NULL,
           trace_id VARCHAR(150) NOT NULL,
           CONSTRAINT item_usage_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE ability_usage
          (id INT NOT NULL AUTO_INCREMENT, 
           date_created VARCHAR(100) NOT NULL,
           steam_id BIGINT NOT NULL,
           match_id BIGINT NOT NULL,
           game_version VARCHAR(100) NOT NULL,
           region VARCHAR(100) NOT NULL,
           hero_id INTEGER NOT NULL,
           hero_name VARCHAR(100) NOT NULL,
           ability_id INTEGER NOT NULL,
           ability_name VARCHAR(100) NOT NULL,
           ability_level INTEGER NOT NULL,
           used_in_game INTEGER NOT NULL,
           trace_id VARCHAR(150) NOT NULL,
           CONSTRAINT ability_usage_pk PRIMARY KEY (id))
          ''')

db_connection.commit()
db_connection.close()