from sqlalchemy import create_engine
import os
import logging
import dotenv


def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


print(f"working directory: {os.getcwd()}")
engine = create_engine(database_connection_url())
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
