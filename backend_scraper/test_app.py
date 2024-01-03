# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI
from src.manga_scraper import *
from data_models.manga_records import *
import json
# from src.manga_scraper_db import *

# uvicorn main:app --reload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def update_manga_list(manga_list: MangaList):
    # Process the manga_list as required
    # For now, let's just return a confirmation message
    print(manga_list)
    return {
        "message": "Successfully confirmed", 
        "url": "http://127.0.0.1:8000/", 
        "confirmation": manga_list
    }

def scrape_record(manga_list):
    """
    Runner function to scrape and do all the backend stuff

    Args:
        manga_list (_type_): _description_

    Returns:
        tuple(db_data, error_list): Returns the db object to be upserted into the backend and the error list to present to frontend.
    """
    error_list = [] # List to store websites that are not supported
    supported_list = [] # List of supported websites. Read from table
    ms = MangaScraper(manga_list)
    for item in ms.manga_list:
        item_base_url = ms.get_base_url(item.link)
        if item_base_url in supported_list:
            # Check what base URL it is and call the correct class
            # For now we use viz and webtoons only
            if "viz" in item_base_url:
                vs = vizScraper(manga_list)
                db_data = vs.create_record(item.link)
            elif "webtoons" in item_base_url:
                ws = webtoonScraper(manga_list)
                db_data = ws.create_record(item.link)        
            else:
                error_list.append(item.link)
    return (db_data, error_list)

def get_new_record(manga_list):
    """
    Create the new records into a new list that we can iterate over and scrape.
    Potentially scrape concurrently for N records.

    Args:
        manga_list (_type_): _description_
    """
    # From the provided manga list
    # Need to identify all the new ones can create new data structure for them
    # These are item's with a "new_" prefix in the ID
    new_list = [item for item in manga_list if "new_" in item.id]
    return new_list

