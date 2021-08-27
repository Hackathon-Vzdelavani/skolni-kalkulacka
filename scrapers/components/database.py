from peewee import *
import os
import sys
from typing import Dict, List, Any


class Program(Model):
    name = CharField()
    faculty = CharField()
    # faculty = ForeignKeyField(Faculty, backref="program")
    catalog_url = CharField()
    #program_type = CharField()
    #length = IntegerField()
    #language = CharField()

"""
class Course(Model):
    name = CharField()
    link = CharField()
    faculty = ForeignKeyField(Faculty, backref="course")
    tags = None
"""

class Skill(Model):
    name = CharField()
    type = CharField()
    skill_type = CharField()


class Database:
    def __init__(self, db_path):
        self.db = SqliteDatabase(database_path, pragmas={'foreign_keys': 1})
        self.bind_db()

    def bind_db(self) -> None:
        """
        Bind the models to the database.
        """
        self.db.bind([Program])   
        self.db.create_tables([Program])
        self.db.close()


    def insert_program(self, data: Dict[str, Any]) -> None:
        program, _ = Program.get_or_create(
            name = data["name"],
            faculty = data["faculty"],
            catalog_url = data["catalog_url"],
        )


    def insert_skill(self) -> None:
        ...


    def insert_course(self) -> None:
        ...


if __name__ == "__main__":
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    database_path = os.path.join(parent_directory, "data", "kalkulacka.db")
    db = Database(database_path)
    db.insert_program({"name":"nameXX", "faculty":"faculty", "catalog_url":"catalog_url"})