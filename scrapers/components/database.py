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


def init_db(db: SqliteDatabase) -> None:
    """
    Bind the models to the database.
    """
    db.bind([Program])   
    db.create_tables([Program])
    db.close()


def insert_program(db: SqliteDatabase, data: Dict[str, Any]) -> None:
    program, _ = Program.get_or_create(
        name = data["name"],
        faculty = data["faculty"],
        catalog_url = data["catalog_url"],
    )


def insert_skill(db: SqliteDatabase) -> None:
    ...


def insert_course(db: SqliteDatabase) -> None:
    db.connect()
    
    return True

if __name__ == "__main__":
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    database_path = os.path.join(parent_directory, "data", "kalkulacka.db")
    db = SqliteDatabase(database_path, pragmas={'foreign_keys': 1})
    init_db(db)
    insert_program(db, {"name":"name", "faculty":"faculty", "catalog_url":"catalog_url"})