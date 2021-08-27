from peewee import *
import os
import sys
from typing import Dict, List, Any

class Program(Model):
    name = CharField()
    faculty = CharField()
    catalogue_url = CharField()
    description = CharField()
    learning = CharField()
    practical = CharField()
    #program_type = CharField()
    #length = IntegerField()
    #language = CharField()


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
            "program_type": None,
            "length": None,
            "language": None,
            "description": None,
            "learning": None,
            "practical": None,
            **data
        }
        if Program.get_or_none(Program.catalog_url == full_data["catalog_url"]):
            query = Program.update(**full_data).where(Program.catalog_url == full_data["catalog_url"])
            query.execute()
        else:
            Program.create(**full_data)
        )


    def insert_skill(self, data: Dict[str, Any]) -> None:
        program, _ = Skill.get_or_create(
            name = data["name"],
            type = data["type"],
            skill_type = data["skill_type"],
        )


if __name__ == "__main__":
    db = Database()


