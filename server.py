from flask import Flask
import json
import threading
import argparse
# from flask_cors import CORS
import sys
import os

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        # CORS(self.app)
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