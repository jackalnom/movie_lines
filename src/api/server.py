from fastapi import FastAPI
from src.api import pkg_util, lines, characters
from src import database as db

app = FastAPI()
app.include_router(characters.router)
app.include_router(lines.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the movie lines API"}
