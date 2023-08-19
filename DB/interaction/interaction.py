import sys
import os
import copy

from DB.client.client import MySQLConnection
from DB.models.models import Base, User, Weeks, Tasks
from DB.exceptions import UserNotFoundException





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
    
    def create_week(self, date):
        week = Weeks(
            date = date,
            tracker_order = [],
            list_order = [[], [], []]
        )
        self.mysql_connection.session.add(week)
        return self.get_week(date)
    
    def create_task(self, task, date, column):
        week = self.mysql_connection.session.query(Weeks).filter_by(date=date).first()
        self.mysql_connection.session.begin()
        task = Tasks(
            task=task,
            status=0,
            week_id=week.id
        )
        self.mysql_connection.session.add(task)
        self.mysql_connection.session.commit()
        a = copy.deepcopy(week.list_order[:])
        while column > len(a) - 1:
            a.append([])
        a[column].append(task.id)
        self.edit_week(date=week.date, list_order=a)
        self.get_week(week.date)
        return self.get_task(task.id)



    def get_week(self, date):
        week = self.mysql_connection.session.query(Weeks).filter_by(date=date).first()
        if week:
            self.mysql_connection.session.expire_all()
            return {"id": week.id, "date": week.date, "tracker_order": week.tracker_order, "list_order": week.list_order}
        
    def get_task(self, task_id):
        task = self.mysql_connection.session.query(Tasks).filter_by(id=task_id).first()
        if task:
            self.mysql_connection.session.expire_all()
            return {"id": task.id, "task": task.task, "status": task.status, "days": task.days, "week_id": task.week_id}
        else:
            raise UserNotFoundException("Task not found")

    def delete_task(self, task_id):
        task = self.mysql_connection.session.query(Tasks).filter_by(id=task_id).first()
        if task:
            self.mysql_connection.session.begin()
            self.mysql_connection.session.delete(task)
            self.mysql_connection.session.commit()
            return "Success", 200
        else:
            return "Error", 404

    def edit_task(self, task_id, task_text=None, status=None, days=None, description=None):
        task = self.mysql_connection.session.query(Tasks).filter_by(id=task_id).first()
        if task:
            if not(task_text is None) and task.task != task_text:
                task.task = task_text
            if not(status is None) and task.status != status:
                task.status = status
            if not(days is None) and task.days != days:
                task.days = days[:]
            if not(description is None) and task.description != description:
                task.description = description
            return self.get_task(task_id=task_id)
        raise UserNotFoundException("Task not found")
    

    def edit_week(self, date, tracker_order=None, list_order=None):
        week = self.mysql_connection.session.query(Weeks).filter_by(date=date).first()
        if week:
            if not(tracker_order is None) and week.tracker_order != tracker_order:
                week.tracker_order = tracker_order
            if not(list_order is None):
                week.list_order = copy.deepcopy(list_order)
            return self.get_week(date)
        else:
            raise UserNotFoundException("Week not found")
    
    def filter_task_for_week_id(self, date):
        week = self.mysql_connection.session.query(Weeks).filter_by(date=date).first()
        tasks = self.mysql_connection.session.query(Tasks).filter_by(week_id=week.id).all()
        return tasks