from sqlalchemy import create_engine
import os
import logging
import csv
import sqlite3
import dotenv
 
def database_connection_url():
    dotenv.load_dotenv()
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


print(f"working directory: {os.getcwd()}")
engine = create_engine(database_connection_url())
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# def sql_data_to_list_of_dicts(path_to_db, select_query):
#     """Returns data from an SQL query as a list of dicts."""
#     try:
#         con = sqlite3.connect(path_to_db)
#         con.row_factory = sqlite3.Row
#         things = con.execute(select_query).fetchall()
#         unpacked = [{k: item[k] for k in item.keys()} for item in things]
#         return unpacked
#     except Exception as e:
#         print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
#         return []
#     finally:
#         con.close()

# lines = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM lines")
# characters = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM characters")
# movies = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM movies")
# conversations = sql_data_to_list_of_dicts("good_movie.db", "SELECT * FROM conversations")

# with open('lines.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames = lines[0].keys())
#     writer.writeheader()
#     writer.writerows(lines)

# with open('characters.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames = characters[0].keys())
#     writer.writeheader()
#     writer.writerows(characters)

# with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames = movies[0].keys())
#     writer.writeheader()
#     writer.writerows(movies)

# with open('conversations.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames = conversations[0].keys())
#     writer.writeheader()
#     writer.writerows(conversations)
