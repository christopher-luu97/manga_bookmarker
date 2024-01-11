# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI
from src.manga_scraper import *
from data_models.manga_records import *
from src.manga_scraper_db import *
import json
from typing import List, Dict
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
    bulk_insert_record(output_list)
    ms_db = MangaScraperDB()
    response = ms_db.get_frontend_data()
    print(f"response: {response}")
    return {
        "message": "Successfully confirmed", 
        "url": "http://127.0.0.1:8000/", 
        "confirmation": response
    }

## TODO: Handling duplicate records that are inserted to the database. Current method just adds new row with new ID even if data is the same
def bulk_insert_record(output_list: List[Dict[str, Any]]):
    """
    Bulk insert records then close at the end

    Args:
        output_list (List[Dict[str, Any]]): _description_
    """
    ms_db = MangaScraperDB()
    for item in output_list:
        manga_name = item["manga_name"]
        print(manga_name)
        manga_id = ms_db.insert_manga(manga_name = manga_name)

        website_id = ms_db.get_website_id(item["website_url"])
        manga_path = item["manga_path"]
        manga_path_id = ms_db.insert_manga_path(manga_id = manga_id, website_id = website_id, manga_path = manga_path)
        manga_chapter_url_id = ms_db.insert_manga_chapter_url_store(record = item, manga_id = manga_id, website_id = website_id, manga_path_id = manga_path_id)
        print(manga_id, website_id, manga_path, manga_path_id, manga_chapter_url_id)
    ms_db.close_connection()

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
    
    new_list = [item for item in manga_list.manga_records if "new_" in item.id]
    return new_list

@app.get("/get_data", response_model=List[Dict[str, Any]])
async def get_data() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    ms_db = MangaScraperDB()
    manga_list = ms_db.get_frontend_data()
    return manga_list

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

    ms_db = MangaScraperDB()
    delete_list = [item for item in manga_list if item.status.lower() == "delete"]

    error_list = []
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