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

## TODO: Handling duplicate records that are inserted to the database. Current method just adds new row with new ID even if data is the same
def bulk_insert_record(output_list: List[Dict[str, Any]], refresh_data:bool):
    """
    Bulk insert records then close at the end

    Args:
        output_list (List[Dict[str, Any]]): _description_
    """
    ms_db = MangaScraperDB()
    for item in output_list:
        manga_name = item["manga_name"]

        # For new additions
        if not(refresh_data):
            similar_manga_id = ms_db.find_similar_manga(manga_name)
            if similar_manga_id is None:
                manga_id = ms_db.insert_manga(manga_name=manga_name)
                website_id = ms_db.get_website_id(item["website_url"])
                manga_path = item["manga_path"]
                manga_path_id = ms_db.insert_manga_path(manga_id = manga_id, website_id = website_id, manga_path = manga_path)
                ms_db.insert_manga_chapter_url_store(record = item, manga_id = manga_id, website_id = website_id, manga_path_id = manga_path_id)
                ms_db.insert_manga_thumbnail(manga_id, website_id, manga_path_id, thumbnail_url=item["manga_thumbnail_url"])
                return "Success!"
            else:
                return(f"Similar manga already exists in the database: {manga_name}. Record was not added. Please delete existing record if you wish to update with a new link.")
        elif refresh_data:  
            manga_id = ms_db.find_similar_manga(manga_name)
            website_id = ms_db.get_website_id(item["website_url"])
            manga_path = item["manga_path"]

            manga_path_id = ms_db.get_manga_path_id(manga_id, website_id, manga_path)
            if manga_path_id is None:
            # Insert new manga path if it doesn't exist
                print("manga_path_id is none")
                manga_path_id = ms_db.insert_manga_path(manga_id=manga_id, website_id=website_id, manga_path=manga_path)

            chapter_url = item["chapter_url"]
            if not ms_db.is_chapter_url_exists(manga_id, website_id, manga_path_id, chapter_url):
                print("new chapter url")
                ms_db.insert_manga_chapter_url_store(record=item, manga_id=manga_id, website_id=website_id, manga_path_id=manga_path_id)

            # Check and insert new manga thumbnail
            thumbnail_url = item["manga_thumbnail_url"]
            if not ms_db.is_thumbnail_exists(manga_id, website_id, manga_path_id, thumbnail_url):
                print("new thumbnail url")
                ms_db.insert_manga_thumbnail(manga_id, website_id, manga_path_id, thumbnail_url=thumbnail_url)

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

def viz_scrape(item: Dict[str, Any], manga_list: list) -> Dict[str, Any]:
    """
    Scrape data for a manga from the Viz website.

    Args:
        item (Dict[str, Any]): A dictionary containing the manga item details.
        manga_list (list): The list of manga records.

    Returns:
        Dict[str, Any]: The scraped data for the manga.
    """
    vs = vizScraper(manga_list)
    return vs.create_record(item.link)

def webtoon_scrape(item: Dict[str, Any], manga_list: list, mk_scraper: MangaKakalotScraper) -> Dict[str, Any]:
    """
    Scrape data for a manga from the Webtoons website and leverage MangaKakalot scraper for thumbnails.

    Args:
        item (Dict[str, Any]): A dictionary containing the manga item details.
        manga_list (list): The list of manga records.
        mk_scraper (MangaKakalotScraper): The MangaKakalot scraper instance.

    Returns:
        Dict[str, Any]: The scraped data for the manga.
    """
    ws = webtoonScraper(manga_list)
    db_data = ws.create_record(item.link)

    # Find manga link in MangaKakalot and extract the thumbnail URL
    search_url = mk_scraper.find_manga_link(search_query=db_data["manga_name"])
    db_data["manga_thumbnail_url"] = mk_scraper.extract_thumbnail(search_url)
    return db_data

def mangakakalot_scrape(item: Dict[str, Any], manga_list: list) -> Dict[str, Any]:
    """
    Scrape data for a manga from the MangaKakalot website.

    Args:
        item (Dict[str, Any]): A dictionary containing the manga item details.
        manga_list (list): The list of manga records.

    Returns:
        Dict[str, Any]: The scraped data for the manga.
    """
    mk = MangaKakalotScraper(manga_list)
    base_url = mk.get_base_url(item.link)
    return mk.create_record(item.link, base_url)

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

@app.get("/get_bookmarks_data", response_model=List[Dict[str, Any]])
async def get_data() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend bookmarks component

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing manga data.
    """
    ms_db = MangaScraperDB()
    manga_list = ms_db.get_bookmarks_data()
    return manga_list

@app.get("/get_supported_websites", response_model=List[Dict[str, Any]])
async def get_data() -> List[Dict[str, Any]]:
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

def scrape_existing_records(manga_list:List[MangaRecord]):
    """
    Scrape existing records in the database and update them as necessary

    Args:
        manga_list (List): List of manga records from the backend.
    """
    error_list = [] # List to store websites that are not supported
    output_list = []
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