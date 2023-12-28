import psycopg2
import uuid
from datetime import datetime
from typing import Dict
import json
from psycopg2 import OperationalError


class MangaScraperAPI:
    """
    Class that connects and performs insertions to the database hosted on PostgreSQL
    """
    def __init__(self):
        try:
            credentials = self.read_db_credentials("db_config.json")
            self.conn = psycopg2.connect(
                host=credentials["host"],
                database=credentials["database"],
                user=credentials["user"],
                password=credentials["password"]
            )
        except OperationalError as e:
            print(f"Error connecting to PostgreSQL database: {e}")
        except (FileNotFoundError, KeyError) as e:
            print(f"Error reading database configuration: {e}")

    @staticmethod
    def read_db_credentials(filename:str):
        """
        Read in database credentials from the .json file

        Args:
            filename (str): name of the .json config file.

        Returns:
            _type_: _description_
        """
        with open(filename, 'r') as file:
            return json.load(file)

    def insert_website(self, website_url:str, website_status:str):
        """
        Insert data into the website table by calling the stored proc

        Args:
            website_url (str): Url of the website
            website_status (str): Status code of the website
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_website(%s, %s, %s, %s)",
                (
                    uuid.uuid4(),
                    website_url,
                    website_status,
                    datetime.now()
                )
            )
            self.conn.commit()

    def insert_manga(self, manga_name:str):
        """
        Insert the manga name into the manga table using the stored proc

        Args:
            manga_name (str): Name of manga to be inserted
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_manga(%s, %s)",
                (
                    uuid.uuid4(),
                    manga_name
                )
            )
            self.conn.commit()

    def insert_manga_path(self, manga_id:str, website_id:str, manga_path:str):
        """
        Insert the website manga path to the appropriate table

        Args:
            manga_id (str): unique id for the manga inserting
            website_id (str): unique id for the website of the manga
            manga_path (str): the manga path as a part of the website
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_manga_path(%s, %s, %s, %s)",
                (
                    uuid.uuid4(),
                    manga_id,
                    website_id,
                    manga_path
                )
            )
            self.conn.commit()

    # TODO: Edit the genre insert as this will be a dictionary containing a list
    def insert_manga_genre(self, manga_id:str, genre:Dict[str]):
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_manga_genre(%s, %s, %s)",
                (
                    uuid.uuid4(),
                    manga_id,
                    genre
                )
            )
            self.conn.commit()

    def insert_manga_name_mapping(self, website_id:str, manga_id:str, manga_name:str):
        """
        Insert the manga name mappings if it exists

        Args:
            website_id (str): Id of where the manga is found on which website
            manga_id (str): The main ID of the manga
            manga_name (str): The alternate name of the manga to be mapped to the main id
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_manga_name_mapping(%s, %s, %s, %s)",
                (
                    uuid.uuid4(),
                    website_id,
                    manga_id,
                    manga_name
                )
            )
            self.conn.commit()

    def insert_manga_chapter_url_store(self, record: Dict, manga_id:str, website_id:str, manga_path_id:str):
        """
        Insert the full link to the latest manga chapter

        Args:
            record (Dict): Dictionary containig all relevant information
            manga_id (str): Relevant manga id
            website_id (str): Relevant Website ID
            manga_path_id (str): Relevant manga path id
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "CALL insert_manga_chapter_url_store(%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    uuid.uuid4(),
                    manga_id,
                    website_id,
                    manga_path_id,
                    record["chapter_url"],
                    record["number_of_pages"],
                    record["chapter_url_status"],
                    record["date_checked"]
                )
            )
            self.conn.commit()

    def close_connection(self):
        """
        Always remember to close the connection if not in use
        """
        if self.conn:
            self.conn.close()
