import sys
import os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask
import json
import threading
import argparse
# from flask_cors import CORS
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from DB.client.client import MySQLConnection

class DbInteraction:
    def __init__(self, host, user, password, db_name, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=host,
            # port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db,
        )
        self.engine = self.mysql_connection.connection.engine
        

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        # CORS(self.app)
        self.db = DbInteraction(
        host="6ocra3.mysql.pythonanywhere-services.com",
        user="6ocra3",
        password="d3e-Gmb-LN8-EnP",
        db_name="6ocra3$planner_db",
        rebuild_db=True
        )
        self.app.add_url_rule("/", view_func=self.hello_world)

    def hello_world(self):
        return {"id": 5}, 200 
# parser = argparse.ArgumentParser()
# parser.add_argument("--config", type=str, dest="config")

# args = parser.parse_args()
# config = config_parser(args.config)

# server_host = config["SERVER_HOST"]
# server_port = config["SERVER_PORT"]
# db_host = "6ocra3.mysql.pythonanywhere-services.com"
# db_port=config["DB_PORT"]
# db_user="6ocra3"
# db_password="d3e-Gmb-LN8-EnP"
# db_name="6ocra3$planner_db"
# rebuild_db = True
server = Server()
app = server.app