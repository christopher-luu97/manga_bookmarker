## This file holds all the models for the API

from pydantic import BaseModel
from typing import Optional

class MangaRecord(BaseModel):
    chapter_number: Optional[int] = None
    id: str
    imageUrl: Optional[str] = None
    lastUpdated: Optional[str] = None
    link: str
    # If status is good then is fine, if status == "Delete" then the user can delete these records from the database
    # We will use the status flag to indicate what database operations to use
    # This flag is changed based on frontend modal operations
    status: str 
    title: str

class MangaList(BaseModel):
    manga_records: list[MangaRecord]
