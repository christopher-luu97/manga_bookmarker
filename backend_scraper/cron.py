# This script calls stored procs to query the database to get some data from the database
from typing import List
from src.manga_scraper_db import MangaScraperDB
from data_models.manga_records import MangaRecord
from test_app import scrape_record, bulk_insert_record


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



def main():
    """
    This method pulls in the data and upserts any new data into bulk insert
    """
    manga_list = get_websites_and_paths()
    processed_data, error_list = scrape_record(manga_list)

    # Handle the errors if needed
    for error in error_list:
        print(f"Error processing {error}")

    # Bulk insert the processed data back into the database
    bulk_insert_record(processed_data)

