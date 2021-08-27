from peewee import *
import os
import sys
from typing import Dict, List, Any


class Program(Model):
    catalog_url = CharField(primary_key=True)
    name = CharField()
    faculty = CharField()
    # faculty = ForeignKeyField(Faculty, backref="program")
    program_type = CharField(null=True)
    length = IntegerField(null=True)
    language = CharField(null=True)


class Course(Model):
    name = CharField()
    link = CharField()
    faculty = CharField()
    # faculty = ForeignKeyField(Faculty, backref="course")
    

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
        full_data = {
            "name": None,
            "faculty": None,
            "catalog_url": None,
            "program_type": None,
            "length": None,
            "language": None,
            **data
        }
        if Program.get_or_none(Program.catalog_url == full_data["catalog_url"]):
            query = Program.update(**full_data).where(Program.catalog_url == full_data["catalog_url"])
            query.execute()
        else:
            Program.create(**full_data)


    def insert_skill(self) -> None:
        ...


    def insert_course(self) -> None:
        ...


if __name__ == "__main__":
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    database_path = os.path.join(parent_directory, "data", "kalkulacka.db")
    db = Database(database_path)
    for i in range(10):
        db.insert_program({"name":f"name{i}", "faculty":"faculty", "catalog_url":f"catalog_url{i}"})
    db.insert_program({"name":f"nameX", "faculty":"faculty", "catalog_url":"catalog_url5"})