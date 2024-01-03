## This file holds all the models for the API

from pydantic import BaseModel

class MangaRecord(BaseModel):
    id: str
    lastChecked: str
    link: str
    status: str
    title: str

class MangaList(BaseModel):
    manga_records: list[MangaRecord]
