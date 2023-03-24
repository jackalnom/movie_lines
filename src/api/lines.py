from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from src import database as db

router = APIRouter()

# Get movie lines with context
@router.get("/lines/{name}")
def say_line(name: str):
    sql = sqlalchemy.text(
        """
        select line_text from 
        characters 
        join lines on characters.character_id = lines.character_id
        where name = :char_name
        ORDER BY RANDOM()
        LIMIT 1
    """
    )

    try:
        with db.engine.connect() as connection:
            dialog = connection.execute(sql, {"char_name": name.upper()}).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="character not found.")

    return {"dialog": dialog}
