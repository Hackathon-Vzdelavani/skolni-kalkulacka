from datetime import datetime
import re
import platform
import getopt
import sys
from unidecode import unidecode
import unidecode

def extract_year_from_url(url):
    return max([int(s) for s in url.split("/") if s.isdigit() and len(s) == 4])

def extract_clean_url(url):
    return re.sub("\?.*", "", url)

def string(value):
    return "'" + str(value) + "'" if value else 'NULL'

def driver_file():
    file_name = "./driver/chromedriver"
    if platform.system() == 'Windows':
        return file_name + '.exe'
    return file_name

def escape_apostrophe(text):
    return text.replace("'", "''")


def remove_diacritics(text):
    return unidecode.unidecode(text)

def error_message(ex):
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    return message

def argument_parser():
    arguments = {}
    passed_arguments = sys.argv[1:]
    for index, arg in enumerate(passed_arguments):
        if index < len(passed_arguments) - 1:
            a, b = arg, passed_arguments[index]
        else:
            a, b = arg, None
        if a.startswith('--') and '=' in a:
            key, val = a.split('=')
            key = key.replace('--', '')
        arguments[key] = val
    return arguments
