# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI
from pydantic import BaseModel
from src.manga_scraper import *
import json
# from src.manga_scraper_db import *

# uvicorn main:app --reload


app = FastAPI()

class MangaData(BaseModel):
    content: str
    submission_type: str


@app.get("/")
async def root(data: MangaData):
    if data.submission_type.lower() == "confirm":
        content = json.loads(data.content)
        # Process the content...
        # Assuming processing is successful
        return {"message": "Successfully confirmed", "url": content, "confirmation": data.submission_type}
    else:
        return {"message": f"Invalid confirmation token requested. Token sent was {data.submission_type}, expecting 'confirm'"}