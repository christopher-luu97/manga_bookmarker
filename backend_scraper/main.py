from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from src.manga_scraper_service import MangaScraperService
from data_models.manga_records import MangaList

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate MangaScraperService
manga_scraper_service = MangaScraperService()

@app.post("/")
async def update_manga_list(manga_list: MangaList):
    """
    Endpoint to update the manga list.

    Args:
        manga_list (MangaList): The manga list to be processed.

    Returns:
        Dict: A dictionary containing the confirmation message, URL, response data, and database upload status.
    """
    # Process the manga_list using MangaScraperService
    output_list, error_list = manga_scraper_service.scrape_record(manga_list)
    insert_record_response = manga_scraper_service.bulk_insert_record(output_list, refresh_data=False)
    manga_scraper_service.delete_record(manga_list)
    response = manga_scraper_service.ms_db.get_frontend_data()

    return {
        "message": "Successfully confirmed", 
        "url": "http://127.0.0.1:8000/", 
        "confirmation": response,
        "db_upload_status": insert_record_response
    }

@app.get("/get_data", response_model=List[Dict[str, Any]])
async def get_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend.
    """
    manga_list = manga_scraper_service.ms_db.get_frontend_data()
    return manga_list

@app.get("/get_bookmarks_data", response_model=List[Dict[str, Any]])
async def get_frontend_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend bookmarks component.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend bookmarks component.
    """
    manga_list = manga_scraper_service.ms_db.get_bookmarks_data()
    return manga_list

@app.get("/get_supported_websites", response_model=List[Dict[str, Any]])
async def get_supported_websites_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend supported websites component within bookmarks.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend supported websites component.
    """
    manga_list = manga_scraper_service.ms_db.get_supported_websites()
    return manga_list

@app.get("/refresh_data")
async def refresh_data():
    """
    Endpoint to refresh data by scraping existing websites for new chapters using MangaScraperService.

    Returns:
        str: A message indicating the status of the data refresh.
    """
    response = manga_scraper_service.refresh_backend_data()
    return response