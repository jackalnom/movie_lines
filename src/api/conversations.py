from fastapi import APIRouter
from src import database as db
from pydantic import BaseModel
from typing import List
import sqlalchemy


class Lines(BaseModel):
    character_id: int
    line_sort: int
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

    """

    # TODO: Make sure all characters are in the movie.
    # TODO: Make sure all lines are in the movie.
    # TODO: Make sure line sort is unique across conversation.
    # TODO: Make sure characters are part of the conversation from the line.

    with db.engine.begin() as conn:
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

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO lines
                (character_id, line_sort, line_text, conversation_id, movie_id)
                VALUES
                (:character_id, :line_sort, :line_text, :conversation_id, :movie_id)
                """
            ),
            [
                {
                    "character_id": line.character_id,
                    "line_sort": line.line_sort,
                    "line_text": line.line_text,
                    "conversation_id": conversation_id,
                    "movie_id": movie_id,
                }
                for line in conversation.lines
            ],
        )

    return {"conversation_id": conversation_id}
