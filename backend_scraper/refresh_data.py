# This script calls stored procs to query the database to get some data from the database
from typing import List, Dict, Any
from src.manga_scraper_db import MangaScraperDB
from data_models.manga_records import MangaRecord
from src.manga_scraper import *
from data_models.manga_records import *
from src.manga_scraper_db import *

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
    if search_url:
        db_data["manga_thumbnail_url"] = mk_scraper.extract_thumbnail(search_url)
    else:
        db_data["manga_thumbnail_url"] = "https://NONE"
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

def get_websites_and_paths() -> List[MangaRecord]:
    """
    Query the database to get a list of websites and their paths.

    Returns:
        List[MangaRecord]: A list of MangaRecord objects with website data.
    """
    ms_db = MangaScraperDB()
    manga_list = []

    try:
        with ms_db.conn.cursor() as cur:
            cur.execute("SELECT * FROM get_website_paths()")
            rows = cur.fetchall()

            for row in rows:
                manga_list.append(MangaRecord(
                    id=str(row[0]),  # Assuming this is the manga_path_id
                    lastChecked="N/A",  # Placeholder, as the actual date is not part of this query
                    link=row[3],  # This is the full path
                    status='Good',  # Assuming default status
                    title=row[2]  
                ))
    except Exception as e:
        print(f"Error querying websites: {e}")

    ms_db.close_connection()
    return manga_list



def refresh_backend_data():
    """
    This method pulls in the data and upserts any new data into bulk insert
    """
    manga_list = get_websites_and_paths()
    processed_data, error_list = scrape_existing_records(manga_list)

    # Handle the errors if needed
    for error in error_list:
        print(f"Error processing {error}")

    bulk_insert_record(processed_data, refresh_data=True)
    response = "Good"
    return response

# if __name__ == "__main__":
#     refresh_backend_data()