from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from src import database as db

router = APIRouter()

@router.get("/characters/{id}")
def get_character(id: str):
    sql = sqlalchemy.text(
        """
        select character_id, name, gender, age, title from 
        characters
        join movies on movies.movie_id = characters.movie_id
        where character_id = :id
        limit 50
    """
    )

    try:
        with db.engine.connect() as connection:
            result = connection.execute(sql, {"id": id})

            for row in result:
                json = ({"character_id": row.character_id,
                         "character": row.name,
                         "movie": row.title,
                         "gender": row.gender,
                         "age": row.age})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="character not found.")

    return json

@router.get("/characters/")
def fuzzy_match_character_names(name: str = ""):
    if name == "":
        return {}

    sql = sqlalchemy.text(
        """
        select character_id, name, title from 
        characters
        join movies on movies.movie_id = characters.movie_id
        where name LIKE :char_name
        limit 50
    """
    )

    try:
        with db.engine.connect() as connection:
            result = connection.execute(sql, {"char_name": f"%{name.upper()}%"})
            json = []
            for row in result:
                json.append({"character_id": row.character_id,
                             "character": row.name,
                             "movie": row.title})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="character not found.")

    return json
