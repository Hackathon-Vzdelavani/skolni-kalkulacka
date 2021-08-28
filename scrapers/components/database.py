from peewee import *
import os
import sys
from typing import Dict, List, Any


class University(Model):
    name = CharField(primary_key=True)


class Faculty(Model):
    name = CharField()


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


class ProgramDetail(Model):
    id = CharField()
    name = CharField()
    code = CharField()
    title = CharField()
    type = CharField()
    form = CharField()
    faculty = CharField()
    length = CharField()
    goal = CharField()
    garant = CharField()
    language = CharField()


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
        database_path = os.path.join(parent_directory, "data", "kalk.sqlite")
        self.db = SqliteDatabase(database_path, pragmas={'foreign_keys': 1})
        self.bind_db()

    def bind_db(self) -> None:
        """
        Bind the models to the database.
        """
        self.db.bind([Program, Skill, ProgramDetail, Course])
        self.db.create_tables([Program, Skill, ProgramDetail, Course])
        self.db.close()

    def insert_program_detail(self, data: Dict[str, Any]) -> None:
        print(data["id"])
        ProgramDetail.create(**data)

    def insert_program(self, data: Dict[str, Any]) -> None:
        full_data = {
            "name": "",
            "faculty": "",
            "catalogue_url": "",
            "specialization_name": "",
            "shortcut": "",
            "specialization_number": "",
            "form": "",
            "type": "",
            "goal": "",
            "annotation": "",
            "length": "",
            "description": "",
            "learning": "",
            "practical": "",
            **data
        }
        Program.create(**full_data)
    
    def update_program(self, data: Dict[str, Any]) -> None:
        if Program.get_or_none(Program.catalog_url == data["catalog_url"]):
            query = Program.update(**data).where(Program.catalog_url == data["catalog_url"])
            query.execute()

    def insert_skill(self, data: Dict[str, Any]) -> None:
        program, _ = Skill.get_or_create(
            name = data["name"],
            type = data["type"],
            skill_type = data["skill_type"],
        )

    def get_program_urls(self):
        query = Program.select(Program.catalogue_url).dicts()
        data = query.execute()
        data = [item["catalogue_url"] for item in data]
        return data


if __name__ == "__main__":
    db = Database()


