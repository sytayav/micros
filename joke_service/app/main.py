import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from database import database as database
from database.database import JokeDB
from model.model import Joke

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.post("/add_joke")
async def add_joke(joke: Joke, db: db_dependency):
    new_joke = JokeDB(**joke.dict())
    db.add(new_joke)
    db.commit()
    db.refresh(new_joke)
    return new_joke


@app.get("/jokes")
async def list_jokes(db: db_dependency):
    return db.query(JokeDB).all()


@app.get("/get_joke_by_id/{joke_id}")
async def get_joke_by_id(joke_id: int, db: db_dependency):
    joke = db.query(JokeDB).filter(JokeDB.id == joke_id).first()
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    return joke


@app.delete("/delete_joke/{joke_id}")
async def delete_joke(joke_id: int, db: db_dependency):
    joke = db.query(JokeDB).filter(JokeDB.id == joke_id).first()
    if not joke:
        raise HTTPException(status_code=404, detail="Joke not found")
    db.delete(joke)
    db.commit()
    return {"message": "Joke deleted successfully"}


@app.get("/search_jokes")
async def search_jokes(query: str, db: db_dependency):
    jokes = db.query(JokeDB).filter(JokeDB.content.ilike(f'%{query}%')).all()
    if not jokes:
        raise HTTPException(status_code=404, detail="No jokes found matching the search criteria")
    return jokes


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
