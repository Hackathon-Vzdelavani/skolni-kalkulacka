from components.database import Database
from spiders.program_parser import ProgramParser
from components.helper import argument_parser

if __name__ == "__main__":
    args = argument_parser(just_key=True)
    if "test_db" in args:
        db = Database()
        db.get_program_urls()
    if "program_parser" in args:
        parser = ProgramParser()
        parser.run()
