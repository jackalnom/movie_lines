from fastapi import APIRouter, HTTPException
import sqlalchemy
from src import database as db
from enum import Enum

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


class movie_sort_options(str, Enum):
    movie_title = "movie_title"
    year = "year"
    rating = "rating"


# Add get parameters
@router.get("/movies/")
def list_movies(
    name: str = "",
    limit: int = 50,
    offset: int = 0,
    sort: movie_sort_options = movie_sort_options.movie_title,
):
    if sort is movie_sort_options.movie_title:
        order_by = db.movies.c.title
    elif sort is movie_sort_options.year:
        order_by = db.movies.c.year
    elif sort is movie_sort_options.rating:
        order_by = sqlalchemy.desc(db.movies.c.imdb_rating)
    else:
        assert False

    stmt = (
        sqlalchemy.select(
            db.movies.c.movie_id,
            db.movies.c.title,
            db.movies.c.year,
            db.movies.c.imdb_rating,
            db.movies.c.imdb_votes,
        )
        .limit(limit)
        .offset(offset)
        .order_by(order_by, db.movies.c.movie_id)
    )

    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.movies.c.title.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = []
        for row in result:
            json.append(
                {
                    "movie_id": row.movie_id,
                    "movie_title": row.title,
                    "year": row.year,
                    "imdb_rating": row.imdb_rating,
                    "imdb_votes": row.imdb_votes,
                }
            )

    return json
