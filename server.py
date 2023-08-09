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
# from DB.client.client import MySQLConnection
class MySQLConnection:
    def __init__(self, host, user, password, db_name, rebuild_db=False):
        self.host = host
        # self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.rebuild_db = rebuild_db
        self.connection = self.connect()
        session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True,
            autoflush=True,
            enable_baked_queries=False,
            expire_on_commit=True        
        )

        self.session = session()



    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name if db_created else ''}"
        )
        return engine.connect()
    
    def connect(self):
        connection = self.get_connection()
        if self.rebuild_db:
            print(1)
            connection.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            connection.execute(f"CREATE DATABASE {self.db_name}")
        return self.get_connection(db_created=True)
    
    def execute_query(self, query):
        res = self.connection.execute(query)
        return res
    
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
        # self.db = DbInteraction(
        # host="6ocra3.mysql.pythonanywhere-services.com",
        # user="6ocra3",
        # password="d3e-Gmb-LN8-EnP",
        # db_name="6ocra3$planner_db",
        # rebuild_db=True
        # )
        self.app.add_url_rule("/", view_func=self.hello_world)

    def hello_world(self):
        return {"id": 5}, 200 
server = Server()
app = server.app