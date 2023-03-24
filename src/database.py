
from sqlalchemy import create_engine
import os
import logging

print(f"working directory: {os.getcwd()}")
engine = create_engine('sqlite:///good_movie.db')
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)