# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI
from src.manga_scraper import *
from data_models.manga_records import *
import json
# from src.manga_scraper_db import *

# uvicorn test_app:app --reload
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

    with open('manga_data.json', 'w') as file:
        file.write(manga_list.json())
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
    supported_list = ["https://www.viz.com", "https://www.webtoons.com"] # List of supported websites. Read from table
    output_list = []
    manga_list = get_new_record(manga_list)
    ms = MangaScraper(manga_list)
    for item in ms.manga_list:
        item_base_url = ms.get_base_url(item.link)
        if item_base_url in supported_list:
            if "viz" in item_base_url:
                vs = vizScraper(manga_list)
                db_data = vs.create_record(item.link)
                output_list.append(db_data)
            elif "webtoons" in item_base_url:
                ws = webtoonScraper(manga_list)
                db_data = ws.create_record(item.link)  
                output_list.append(db_data)
        else:
            error_list.append(item.link)
    return (output_list, error_list)

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

def insert_records(output_list):
    """
    Method to call the mangaScraperDB class to perform DB operations

    Args:
        output_list (_type_): _description_
    """
    pass

def get_data():
    """
    API for frontend to call from server to populate everyday
    """
    pass
