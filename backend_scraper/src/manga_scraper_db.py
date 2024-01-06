import psycopg2
import uuid
from datetime import datetime
from typing import Dict
import json
from psycopg2 import OperationalError


class MangaScraperDB:
    """
    Class that connects and performs insertions to the database hosted on PostgreSQL
    """
    def __init__(self):
        try:
            #credentials = self.read_db_credentials("/secrets/db_config.json") ## To change into environ reading
            self.conn = psycopg2.connect(
                host= "localhost", # credentials["host"],
                database= "manga_tracker", # credentials["database"],
                user="postgres", # credentials["user"],
                password="Password" # credentials["password"]
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
        website_id = str(uuid.uuid4())
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_website(%s, %s, %s, %s)",
                            (website_id, 
                             website_url, 
                             website_status, 
                             datetime.now()))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_website: {e}")
            self.conn.rollback()
        return website_id 

    def insert_manga(self, manga_name:str):
        """
        Insert the manga name into the manga table using the stored proc

        Args:
            manga_name (str): Name of manga to be inserted
        """
        manga_id = str(uuid.uuid4())
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_manga(%s, %s)", 
                            (manga_id, 
                             manga_name))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_manga: {e}")
            self.conn.rollback()
        return manga_id

    def insert_manga_path(self, manga_id:str, website_id:str, manga_path:str):
        """
        Insert the website manga path to the appropriate table

        Args:
            manga_id (str): unique id for the manga inserting
            website_id (str): unique id for the website of the manga
            manga_path (str): the manga path as a part of the website
        """
        manga_path_id = str(uuid.uuid4())
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_manga_path(%s, %s, %s, %s)", 
                            (manga_path_id, 
                             manga_id, 
                             website_id, 
                             manga_path))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_manga_path: {e}")
            self.conn.rollback()
        return manga_path_id

    # TODO: Edit the genre insert as this will be a dictionary containing a list
    def insert_manga_genre(self, manga_id:str, genre:Dict):
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_manga_genre(%s, %s, %s)", 
                            (str(uuid.uuid4()), 
                             manga_id, 
                             genre))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_manga_genre: {e}")
            self.conn.rollback()

    def insert_manga_name_mapping(self, website_id:str, manga_id:str, manga_name:str):
        """
        Insert the manga name mappings if it exists

        Args:
            website_id (str): Id of where the manga is found on which website
            manga_id (str): The main ID of the manga
            manga_name (str): The alternate name of the manga to be mapped to the main id
        """
        manga_name_mapping_id = str(uuid.uuid4())
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_manga_name_mapping(%s, %s, %s, %s)", 
                            (manga_name_mapping_id, 
                             website_id, 
                             manga_id, 
                             manga_name))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_manga_name_mapping: {e}")
            self.conn.rollback()
        return manga_name_mapping_id

    def insert_manga_chapter_url_store(self, record: Dict, manga_id:str, website_id:str, manga_path_id:str):
        """
        Insert the full link to the latest manga chapter

        Args:
            record (Dict): Dictionary containig all relevant information
            manga_id (str): Relevant manga id
            website_id (str): Relevant Website ID
            manga_path_id (str): Relevant manga path id
        """
        manga_chapter_url_id = str(uuid.uuid4())
        try:
            with self.conn.cursor() as cur:
                cur.execute("CALL insert_manga_chapter_url_store(%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (manga_chapter_url_id, 
                         manga_id, 
                         website_id, 
                         manga_path_id,
                         record["chapter_url"], 
                         int(record["number_of_pages"]),  # Ensure this is an integer
                         str(record["chapter_url_status"]), 
                         datetime.strptime(record["date_checked"], '%Y-%m-%d %H:%M:%S')  # Parse to datetime object
                        ))
                self.conn.commit()
        except Exception as e:
            print(f"Error in insert_manga_chapter_url_store: {e}")
            self.conn.rollback()
        return manga_chapter_url_id
    
    def get_website_id(self, website_url: str) -> str:
        """
        Retrieve the website ID for a given website URL.

        Args:
            website_url (str): URL of the website

        Returns:
            str: The website ID or None if not found
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT get_website_id_by_url(%s)", (website_url,))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    return None
        except Exception as e:
            print(f"Error in get_website_id: {e}")
            return None

    def close_connection(self):
        """
        Always remember to close the connection if not in use
        """
        if self.conn:
            self.conn.close()
