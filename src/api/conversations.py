from fastapi import APIRouter, HTTPException
from src import database as db
from pydantic import BaseModel
from typing import List
import sqlalchemy


class Lines(BaseModel):
    character_id: int
    line_text: str


class Conversation(BaseModel):
    character_1_id: int
    character_2_id: int
    lines: List[Lines]


router = APIRouter()


@router.post("/movies/{movie_id}/conversations/", tags=["movies"])
def add_conversation(movie_id: int, conversation: Conversation):
    """
    This endpoint adds a conversation to a movie. The conversation is represented
    by the two characters involved in the conversation and a series of lines between
    those characters in the movie.

    The endpoint ensures that all characters are part of the referenced movie,
    that the characters are not the same, and that the lines of a conversation
    match the characters involved in the conversation.

    Line sort is set based on the order in which the lines are provided in the
    request body.

    The endpoint returns the id of the resulting conversation that was created.
    """

    with db.engine.begin() as conn:
        for line in conversation.lines:
            if line.character_id not in [
                conversation.character_1_id,
                conversation.character_2_id,
            ]:
                raise HTTPException(
                    status_code=422, detail="Character is not part of conversation."
                )

        characters_in_movie = conn.execute(
            sqlalchemy.text(
                """
                SELECT COUNT(*)
                FROM
                characters
                WHERE
                movie_id = :movie_id AND
                character_id IN (:character1_id, :character2_id)
                """
            ),
            [
                {
                    "character1_id": conversation.character_1_id,
                    "character2_id": conversation.character_2_id,
                    "movie_id": movie_id,
                }
            ],
        ).scalar_one()

        if characters_in_movie != 2:
            raise HTTPException(
                status_code=422, detail="Characters are not in given movie."
            )

        conversation_id = conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO conversations (character1_id, character2_id, movie_id)
                VALUES (:character1_id, :character2_id, :movie_id)
                RETURNING conversation_id
                """
            ),
            [
                {
                    "character1_id": conversation.character_1_id,
                    "character2_id": conversation.character_2_id,
                    "movie_id": movie_id,
                }
            ],
        ).scalar_one()

        line_sort = 0
        lines = []
        for line in conversation.lines:
            lines.append(
                {
                    "character_id": line.character_id,
                    "line_sort": line_sort,
                    "line_text": line.line_text,
                    "conversation_id": conversation_id,
                    "movie_id": movie_id,
                }
            )
            line_sort += 1

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO lines
                (character_id, line_sort, line_text, conversation_id, movie_id)
                VALUES
                (:character_id, :line_sort, :line_text, :conversation_id, :movie_id)
                """
            ),
            lines,
        )

    return {"conversation_id": conversation_id}
