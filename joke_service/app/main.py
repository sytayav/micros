import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from sqlalchemy.orm import Session
from typing import Annotated, List
from keycloak import KeycloakOpenID
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

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                 client_id=KEYCLOAK_CLIENT_ID,
                                 realm_name=KEYCLOAK_REALM,
                                 client_secret_key=KEYCLOAK_CLIENT_SECRET)


@app.post("/get_token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")


def chechnya_for_role(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (chechnya_for_role(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"


@app.post("/add_joke")
async def add_joke(joke: Joke, db: db_dependency, token: str = Header()):
    if (chechnya_for_role(token)):
        new_joke = JokeDB(**joke.dict())
        db.add(new_joke)
        db.commit()
        db.refresh(new_joke)
        return new_joke
    else:
        return "Wrong JWT Token"


@app.get("/jokes")
async def list_jokes(db: db_dependency, token: str = Header()):
    if (chechnya_for_role(token)):
        return db.query(JokeDB).all()
    else:
        return "Wrong JWT Token"


@app.get("/get_joke_by_id/{joke_id}")
async def get_joke_by_id(joke_id: int, db: db_dependency, token: str = Header()):
    if (chechnya_for_role(token)):
        joke = db.query(JokeDB).filter(JokeDB.id == joke_id).first()
        if not joke:
            raise HTTPException(status_code=404, detail="Joke not found")
        return joke
    else:
        return "Wrong JWT Token"


@app.delete("/delete_joke/{joke_id}")
async def delete_joke(joke_id: int, db: db_dependency, token: str = Header()):
    if (chechnya_for_role(token)):
        joke = db.query(JokeDB).filter(JokeDB.id == joke_id).first()
        if not joke:
            raise HTTPException(status_code=404, detail="Joke not found")
        db.delete(joke)
        db.commit()
        return {"message": "Joke deleted successfully"}
    else:
        return "Wrong JWT Token"


@app.get("/search_jokes")
async def search_jokes(query: str, db: db_dependency, token: str = Header()):
    if (chechnya_for_role(token)):
        jokes = db.query(JokeDB).filter(JokeDB.content.ilike(f'%{query}%')).all()
        if not jokes:
            raise HTTPException(status_code=404, detail="No jokes found matching the search criteria")
        return jokes
    else:
        return "Wrong JWT Token"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
