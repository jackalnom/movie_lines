from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from src import database as db

router = APIRouter()


@router.get("/characters/{name}")
def fuzzy_match_character_names(name: str):
    sql = sqlalchemy.text(
        """
        select name, title from 
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
                json.append({"character": row.name,
                             "movie": row.title})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="character not found.")

    return json
