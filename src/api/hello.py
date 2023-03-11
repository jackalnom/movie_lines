from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from src import database as db

router = APIRouter()


@router.get("/hello/{name}")
def say_hello(name: str):
    sql = sqlalchemy.text(
        """
    select dialog from lotr
    where char = :char_name
    ORDER BY random()
    LIMIT 1
    """
    )

    try:
        with db.engine.connect() as connection:
            dialog = connection.execute(sql, {"char_name": name.upper()}).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="LOTR character not found.")

    return {"dialog": dialog}
