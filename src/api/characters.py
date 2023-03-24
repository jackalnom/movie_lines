from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy.orm.exc import NoResultFound
from src import database as db
from enum import Enum

router = APIRouter()

@router.get("/characters/{id}")
def get_character(id: str):
    character_sql = sqlalchemy.text(
        """
        select character_id, name, gender, title from 
        characters
        join movies on movies.movie_id = characters.movie_id
        where character_id = :id
        limit 50
    """
    )

    conversations_sql = sqlalchemy.text(
        """
        select * from
        (select character1_id character_id, name, gender, COUNT(*) num_lines
        from conversations
        join characters ON character1_id = characters.character_id
        join lines ON lines.conversation_id = conversations.conversation_id
        WHERE character2_id = :id
        GROUP BY character1_id, name
        order by num_lines desc)
        UNION ALL
        select * from
        (select character2_id character_id, name, gender, COUNT(*) num_lines
        from conversations
        join characters ON character2_id = characters.character_id
        join lines ON lines.conversation_id = conversations.conversation_id
        WHERE character1_id = :id
        GROUP BY character2_id, name
        order by num_lines desc)
        order by num_lines desc
        limit 5
        """
    )

    try:
        with db.engine.connect() as connection:
            conversationResult = connection.execute(conversations_sql, {"id": id})
            conversation_json = []
            for row in conversationResult:
                conversation_json.append({"character_id": row.character_id,
                         "character": row.name,
                         "gender": row.gender,
                         "number_of_lines_together": row.num_lines})

            result = connection.execute(character_sql, {"id": id})

            for row in result:
                json = ({"character_id": row.character_id,
                         "character": row.name,
                         "movie": row.title,
                         "gender": row.gender,
                         "top_conversations": conversation_json})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="character not found.")

    return json

class character_sort_options(str, Enum):
    character = 'character'
    movie = 'movie'
    number_of_lines = 'number_of_lines'

@router.get("/characters/")
def list_characters(name: str = "", 
                    limit: int = 50, 
                    offset: int = 0, 
                    sort: character_sort_options = character_sort_options.character):
    metadata_obj = sqlalchemy.MetaData()
    characters = sqlalchemy.Table("characters", metadata_obj, autoload_with=db.engine)
    movies = sqlalchemy.Table("movies", metadata_obj, autoload_with=db.engine)
    lines = sqlalchemy.Table("lines", metadata_obj, autoload_with=db.engine)

    subquery = sqlalchemy.select(lines.c.character_id, 
                                 sqlalchemy.func.count("*").label('num_lines')
                                 )\
                                .group_by(lines.c.character_id).subquery()

    if sort is character_sort_options.character:
        order_by = characters.c.name
    elif sort is character_sort_options.movie:
        order_by = movies.c.title
    elif sort is character_sort_options.number_of_lines:
        order_by = sqlalchemy.desc(subquery.c.num_lines)
    else:
        assert False

    stmt = sqlalchemy.select(characters.c.name, 
                              characters.c.character_id, 
                              movies.c.title,
                              subquery.c.num_lines).join(movies).join(subquery).limit(limit).offset(offset).order_by(order_by)
                              
    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(characters.c.name.ilike(f"%{name}%"))
    
    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append({"character_id": row.character_id,
                            "character": row.name,
                            "movie": row.title,
                            "number_of_lines": row.num_lines})

    return json
