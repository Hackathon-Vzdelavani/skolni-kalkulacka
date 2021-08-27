import sqlite3
from sqlite3 import Error
import os
from components.logger import Logger
parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class SqliteDatabase:
    def __init__(self):
        self.logger = Logger("db").logger
        self.create_connection()

    def create_connection(self):
        db_file = os.path.join(parent_directory, "data", "kalkulacka.db")
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_programs(self):
        try:
            query_text = """SELECT * FROM program"""
            self.cursor.execute(query_text)
        except Exception as e:
            self.logger.error(str(e))
        result = self.cursor.fetchall()
        return result

    def insert_program(self, item):
        try:
            query = ("INSERT INTO program (url, name, faculty, tags) "
                     "VALUES (%s,%s,%s,%s)")
            self.cursor.execute(query, [item["url"],item["name"],item["faculty"],item["tags"]])
            self.connection.commit()
        except Exception as e:
            self.logger.error(item["name"] + ': ' + str(e))
            self.connection.rollback()



if __name__ == '__main__':
    db = SqliteDatabase()
    db.create_connection()
