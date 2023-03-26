from fastapi import APIRouter, HTTPException
import sqlalchemy
from src import database as db

router = APIRouter()


# include top 3 actors by number of lines
@router.get("/movies/{movie_id}")
def get_movie(movie_id: str):
    sql = sqlalchemy.text(
        """
        select * from (
        select movies.movie_id, title,
        characters.character_id, characters.name, num_lines,
        ROW_NUMBER() OVER (ORDER BY num_lines desc) as row 
        from
        movies
        join characters on characters.movie_id = movies.movie_id
        join (
            select count(*) num_lines, character_id from lines group by character_id
            ) lines
        ON characters.character_id = lines.character_id
        where movies.movie_id = :movie_id
        order by num_lines desc
        ) AS sq2 where row <= 5
    """
    )

    with db.engine.connect() as connection:
        result = connection.execute(sql, {"movie_id": movie_id})
        character_json = []
        movie_json = None
        for row in result:
            if movie_json is None:
                movie_json = {
                    "movie_id": row.movie_id,
                    "title": row.title,
                    "top_characters": character_json,
                }

            character_json.append(
                {
                    "character_id": row.character_id,
                    "character": row.name,
                    "num_lines": row.num_lines,
                }
            )

        if movie_json is None:
            raise HTTPException(status_code=404, detail="movie not found.")

        return movie_json


# TODO: Mean age of characters by gender weighted by number of lines.


# Add get parameters
@router.get("/movies/")
def list_movies(limit: int = 50, offset: int = 0):
    sql = sqlalchemy.text(
        """
        select movie_id, title from
        movies
        order by movie_id asc
        limit :limit
        offset :offset

    """
    )

    json = []
    with db.engine.connect() as connection:
        result = connection.execute(sql, {"limit": limit, "offset": offset})
        ## create links to top 10 characters by number of lines
        for row in result:
            json.append({"movie_id": row.movie_id, "title": row.title})

    return json
