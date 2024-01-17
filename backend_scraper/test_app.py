# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI
from src.manga_scraper import *
from data_models.manga_records import *
from src.manga_scraper_db import *
import json
from refresh_data import *
from typing import List, Dict, Any
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

    # with open('manga_data.json', 'w') as file:
    #     file.write(manga_list.json())
    output_list, error_list = scrape_record(manga_list)
    insert_record_response = bulk_insert_record(output_list, refresh_data=False)
    delete_record(manga_list)
    ms_db = MangaScraperDB()
    response = ms_db.get_frontend_data()
    return {
        "message": "Successfully confirmed", 
        "url": "http://127.0.0.1:8000/", 
        "confirmation": response,
        "db_upload_status": insert_record_response
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
    output_list = []
    manga_list = get_new_record(manga_list)
    ms = MangaScraper(manga_list)
    mk_scraper = MangaKakalotScraper(manga_list)
    for item in ms.manga_list:
        item_base_url = ms.get_base_url(item.link)
        if "viz" in item_base_url:
            db_data = viz_scrape(item, manga_list)
            output_list.append(db_data)
        elif "webtoons" in item_base_url:
            db_data = webtoon_scrape(item, manga_list, mk_scraper)
            output_list.append(db_data)
        elif "chapmanganato" in item_base_url:
            db_data = mangakakalot_scrape(item, manga_list)
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
    
    new_list = [item for item in manga_list.manga_records if "new_" in item.id]
    return new_list

@app.get("/get_data", response_model=List[Dict[str, Any]])
async def get_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    ms_db = MangaScraperDB()
    manga_list = ms_db.get_frontend_data()
    return manga_list

@app.get("/get_bookmarks_data", response_model=List[Dict[str, Any]])
async def get_frontend_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend bookmarks component

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    ms_db = MangaScraperDB()
    manga_list = ms_db.get_bookmarks_data()
    return manga_list

@app.get("/get_supported_websites", response_model=List[Dict[str, Any]])
async def get_supported_websites_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend supported websites component within bookmarks

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    ms_db = MangaScraperDB()
    manga_list = ms_db.get_supported_websites()
    return manga_list

@app.get("/refresh_data")
async def refresh_data():
    """
    Endpoint to scrape existing websites for new chapters

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    response = refresh_backend_data()
    return response

## TODO: Migrate delete record to the ms_db class
def delete_record(manga_list: List[MangaRecord]) -> List[Dict[str, str]]:
    """
    Deletes records from the database for each manga in the provided list that is marked with the status 'Delete'.

    This function iterates over the provided manga list, checks for the status of each manga record, and if the
    status is 'Delete', it proceeds to call a stored procedure to remove the corresponding records from various
    related database tables.

    Args:
        manga_list (List[MangaRecord]): A list of MangaRecord objects, each representing a manga record.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing error messages for any manga records that failed
                              to be deleted. Each dictionary includes the 'id' of the manga and the 'error' message.
    """

    delete_list = [item for item in manga_list.manga_records if item.status.lower() == "delete"]
    error_list = []
    if len(delete_list) >0: # Only run if the data exists
        ms_db = MangaScraperDB()
        # We know the data can be deleted because the data is grabbed from the backend to be presented to the frontend
        # This frontend data is then sent as part of the response when updating records
        for item in delete_list:
            try:
                with ms_db.conn.cursor() as cur:
                    cur.execute("CALL delete_manga_record(%s)", (item.id,))
                    ms_db.conn.commit()
            except Exception as e:
                error_list.append({"id": item.id, "error": str(e)})
                ms_db.conn.rollback()

        ms_db.close_connection()
    return error_list