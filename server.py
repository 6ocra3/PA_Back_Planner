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
from DB.interaction.interaction import DbInteraction

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
        return {"id": 6}, 200 
server = Server()
app = server.app