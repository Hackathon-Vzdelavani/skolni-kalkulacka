from peewee import *
import os
import sys
from typing import Dict, List, Any

"""
class University(Model):
    name = CharField(primary_key=True)


class Faculty(Model):
    name = CharField()
"""

class Program(Model):
    name = CharField()
    faculty = CharField()
    catalogue_url = CharField()
    specialization_name = CharField()
    specialization_number = CharField()
    shortcut = CharField()
    form = CharField()
    type = CharField()
    goal = CharField()
    annotation = CharField()
    length = CharField()
    description = CharField()
    learning = CharField()
    practical = CharField()


class Course(Model):
    name = CharField()
    goals = TextField()
    requirements = TextField()
    contents = TextField()
    faculty = CharField()
    # faculty = ForeignKeyField(Faculty, backref="course")


class Skill(Model):
    name = CharField()
    type = CharField()
    skill_type = CharField()


class Database:
    def __init__(self):
        parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        database_path = os.path.join(parent_directory, "data", "db.sqlite")
        self.db = SqliteDatabase(database_path, pragmas={'foreign_keys': 1})
        self.bind_db()

    def bind_db(self) -> None:
        """
        Bind the models to the database.
        """
        self.db.bind([Program, Skill])
        self.db.create_tables([Program, Skill])
        self.db.close()

    def insert_program(self, data: Dict[str, Any]) -> None:
        full_data = {
            "name": None,
            "faculty": None,
            "catalogue_url": None,
            "specialization_name"
            "shortcut": None,
            "specialization_number": None,
            "form": None,
            "type": None,
            "goal": None,
            "annotation": None,
            "length": None,
            "description": None,
            "learning": None,
            "practical": None,
            **data
        }
        Program.create(**full_data)
    
    def update_program(self, data: Dict[str, Any]):
        query = Program.update(**data).where(Program.catalog_url == data["catalogue_url"])
        query.execute()

    def insert_skill(self, data: Dict[str, Any]) -> None:
        program, _ = Skill.get_or_create(
            name = data["name"],
            type = data["type"],
            skill_type = data["skill_type"],
        )

    def get_programs(self):
        query = Program.get()
        query.execute()


if __name__ == "__main__":
    db = Database()


