from fastapi import FastAPI
from src.api import pkg_util, hello
from src import database as db

app = FastAPI()
app.include_router(hello.router)
app.include_router(pkg_util.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the LOTR dialog responder"}
