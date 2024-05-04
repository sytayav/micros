import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'Service alive'}


@app.get("/random_joke")
async def get_random_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Error retrieving joke")


@app.get("/jokes_by_category/{category}")
async def get_jokes_by_category(category: str):
    url = f"https://v2.jokeapi.dev/joke/{category}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Error retrieving jokes")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
