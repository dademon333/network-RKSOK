import os

from dotenv import load_dotenv

load_dotenv()


class Tokens:
    PSQL_USER = os.getenv('PSQL_USER')
    PSQL_PASSWORD = os.getenv('PSQL_PASSWORD')
    PSQL_HOST = os.getenv('PSQL_HOST')
    PSQL_PORT = os.getenv('PSQL_PORT')
    PSQL_DATABASE = os.getenv('PSQL_DATABASE')
