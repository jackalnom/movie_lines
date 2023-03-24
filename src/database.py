import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

print(f"working directory: {os.getcwd()}")
engine = create_engine('sqlite:///good_movie.db')
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)