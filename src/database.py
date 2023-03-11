import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def sql_data_to_list_of_dicts(path_to_db, select_query):
    """Returns data from an SQL query as a list of dicts."""
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        things = con.execute(select_query).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()

lines = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM lines")
characters = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM characters")
movies = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM movies")

print(f"working directory: {os.getcwd()}")
engine = create_engine('sqlite:///good_movie.db')