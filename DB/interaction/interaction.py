import sys
import os
import copy

from DB.client.client import MySQLConnection
from DB.models.models import Base, User, Weeks, Tasks






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
        if rebuild_db:         
            self.create_table_weeks()
            self.create_table_tasks()

    def create_table_tasks(self):
        if not self.engine.dialect.has_table(self.engine, "tasks"):
            Base.metadata.tables["tasks"].create(self.engine)
        else:
            self.mysql_connection.execute_query("DROP TABLE IF EXISTS tasks")
            Base.metadata.tables["tasks"].create(self.engine)
    
    def create_table_weeks(self):
        if not self.engine.dialect.has_table(self.engine, "weeks"):
            Base.metadata.tables["weeks"].create(self.engine)
        else:
            self.mysql_connection.execute_query("DROP TABLE IF EXISTS weeks")
            Base.metadata.tables["weeks"].create(self.engine)