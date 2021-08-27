from peewee import *
import os
import sys


class Program(Model):
    name = CharField()
    faculty = ForeignKeyField(Faculty, backref="program")
    catalogue_url = CharField()
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
    db.bind([University, Faculty, Program, Course])   
    db.create_tables([University, Faculty, Program, Course])
    db.close()


def insert_skill(db: SqliteDatabase) -> None:
    ...

def insert_course(db: SqliteDatabase) -> None:
    db.connect()
    
    return True



if __name__ == "__main__":
    parent_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    database_path = os.path.join(parent_directory, "data", "kalkulacka.db")
    db = SqliteDatabase(database_path, pragmas={'foreign_keys': 1})
