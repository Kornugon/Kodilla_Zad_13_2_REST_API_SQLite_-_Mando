import os
import json

import sqlite3
from sqlite3 import Error

from models import datas

SAVED_FOLDER_NAME = 'Saved'
FILE_NAME = "mando.db"
FILE_PATH = os.path.join(SAVED_FOLDER_NAME, FILE_NAME)



class TodosSQLite():
    def __init__(self, db_file):
        self.db_file = db_file


    def create_connection(self):
        with sqlite3.connect(self.db_file) as self.conn:
            return self.conn


    def execute_sql(self, sql):
        """
        Create Table or add task
        """
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)


    def add_episode(self, episode):
        sql = '''INSERT INTO episodes(title, description)
                VALUES(?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, episode)
        self.conn.commit()
        return cur.lastrowid


    def add_task(self, task):
        sql = '''INSERT INTO tasks(episode_id, task, task_description, status, start_date, end_date)
                VALUES(?,?,?,?,?,?)'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return cur.lastrowid


    def load_task(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks")
        rows = cur.fetchall()
        print(rows)
        return rows


    def select_task_by_status(self, status):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE status=?", (status,))

        rows = cur.fetchall()
        return rows


    def select_all(self, table):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows


    def select_where(self, table, **query):
        cur = self.conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows


    def update(self, table, id, **kwargs):
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
                    SET {parameters}
                    WHERE id = ?'''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            self.conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)


    def delete_where(self, table, **kwargs):
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()
        return "Deleted"


    def delete_all(self, table):
        sql = f'DELETE FROM {table}'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return f'Table {table} cleared'


    def load_episodes_JSON_backup(self):
        self.delete_all("episodes")
        self.delete_all("tasks")

        for epi in datas:
            title = epi["title"]
            description = epi["description"]
            viewed = epi["viewed"]
            id = epi["id"]
            episode = (title, description)

            self.add_episode(episode)
            
            if viewed:
                task = (
                        id,
                        "Obejrzyj",
                        "Obejrzyj odcinek",
                        "done",
                        "2021-01-15 12:00:00",
                        "2021-01-15 15:00:00"
                        )
            else:
                task = (
                        id,
                        "Obejrzyj",
                        "Obejrzyj odcinek",
                        "open",
                        "2021-01-15 12:00:00",
                        "2021-01-15 15:00:00"
                        )
            
            self.add_task(task)
        return "Episodes and tasks restored from JSON backup"


episodes = TodosSQLite(db_file=FILE_PATH)


