from typing import List, Dict, Any, Tuple
from src.manga_scraper import MangaScraper, MangaKakalotScraper, vizScraper, webtoonScraper
from data_models.manga_records import MangaList, MangaRecord
from src.manga_scraper_db import MangaScraperDB

class MangaScraperService:
    def __init__(self):
        self.ms_db = MangaScraperDB()

    def scrape_record(self, manga_list: MangaList) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
        """
        Runner function to scrape and do all the backend stuff

        Args:
            manga_list (_type_): List of manga

        Returns:
            tuple(db_data, error_list): Returns the db object to be upserted into the backend and the error list to present to frontend.
        """
        error_list = [] # List to store websites that are not supported
        output_list = []
        manga_list = self.get_new_record(manga_list)
        ms = MangaScraper(manga_list)
        mk_scraper = MangaKakalotScraper(manga_list)
        for item in ms.manga_list:
            item_base_url = ms.get_base_url(item.link)
            if "viz" in item_base_url:
                db_data = self.viz_scrape(item, manga_list)
                output_list.append(db_data)
            elif "webtoons" in item_base_url:
                db_data = self.webtoon_scrape(item, manga_list, mk_scraper)
                output_list.append(db_data)
            elif "chapmanganato" in item_base_url:
                db_data = self.mangakakalot_scrape(item, manga_list)
                output_list.append(db_data)
            else:
                error_list.append(item.link)

        return (output_list, error_list)

    def get_new_record(self, manga_list: MangaList) -> List[MangaRecord]:
        """
        Create the new records into a new list that we can iterate over and scrape.
        Potentially scrape concurrently for N records.

        Args:
            manga_list (MangaList): List of manga
        """
        # From the provided manga list
        # Need to identify all the new ones can create new data structure for them
        # These are item's with a "new_" prefix in the ID
        
        new_list = [item for item in manga_list.manga_records if "new_" in item.id]
        return new_list

    def viz_scrape(self, item: Dict[str, Any], manga_list: List[MangaRecord]) -> Dict[str, Any]:
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

    def webtoon_scrape(self, item: Dict[str, Any], manga_list: List[MangaRecord], mk_scraper: MangaKakalotScraper) -> Dict[str, Any]:
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

    def mangakakalot_scrape(self, item: Dict[str, Any], manga_list: List[MangaRecord]) -> Dict[str, Any]:
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

    def bulk_insert_record(self, output_list: List[Dict[str, Any]], refresh_data: bool) -> str:
        """
        Bulk insert records then close at the end

        Args:
            output_list (List[Dict[str, Any]]): List of results to be inserted into the database
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

    def delete_record(self, manga_list: List[MangaRecord]) -> List[Dict[str, str]]:
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

    def refresh_backend_data(self) -> str:
        """
        This method pulls in the data and upserts any new data into bulk insert
        """
        manga_list = self.get_websites_and_paths()
        processed_data, error_list = self.scrape_existing_records(manga_list)

        # Handle the errors if needed
        for error in error_list:
            print(f"Error processing {error}")

        self.bulk_insert_record(processed_data, refresh_data=True)
        response = "Good"
        return response

    def get_websites_and_paths(self) -> List[MangaRecord]:
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
                        id=str(row[0]),
                        lastChecked="N/A",
                        link=row[3],
                        status='Good',
                        title=row[2]  
                    ))
        except Exception as e:
            print(f"Error querying websites: {e}")

        ms_db.close_connection()

    def scrape_existing_records(self, manga_list: List[MangaRecord]) -> Tuple[List[Dict[str, Any]], List[str]]:
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
                db_data = self.viz_scrape(item, manga_list)
                output_list.append(db_data)
            elif "webtoons" in item_base_url:
                db_data = self.webtoon_scrape(item, manga_list, mk_scraper)
                output_list.append(db_data)
            elif "chapmanganato" in item_base_url:
                db_data = self.mangakakalot_scrape(item, manga_list)
                output_list.append(db_data)
            else:
                error_list.append(item.link)

        return (output_list, error_list)