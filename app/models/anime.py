from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from pymongo import IndexModel, ASCENDING, DESCENDING

from datetime import datetime


from typing import Optional, List


class Anime(Document):
    title: str
    year_of_release: Optional[datetime] = datetime.now()
    creator: str
    number_of_episodes: Optional[int] = 0

    class Settings:
        name = "anime"
        indexes = [
            IndexModel([("title", DESCENDING)])
        ]

    class Config:
        schema_extra = {
            "examples": {
                "title": "The Messanger from the Abyss",
                "year_of_release": datetime.now(),
                "creator": "Bad Player Studios"
            }
        }


class AnimeUpdate(BaseModel):
    title: Optional[str]
    creator: Optional[str]


class AnimeResponse(BaseModel):
    # id: PydanticObjectId
    title: str
    year_of_release: datetime
    creator: str


class Season(Document):
    anime_title: str
    season_number: int
    description: Optional[str] = None

    class Setting:
        name = "season"
        indexes = [
            IndexModel([("season_number", ASCENDING)])
        ]

    class Config:
        schema_extra = {
            "examples": {
                "anime": "The Messanger from the Abyss",
                "episodes": [1, 2, 3, 4, 5],
                "season_number": 1,
                "description": "If inspired by my anime title, do me a favor and write the whole"
                               "story. I will have it published"
            }
        }


class Episode(Document):
    anime_title: str | Anime
    season: str | Season
    epi_title: str
    epi_number: int
    created: Optional[datetime] = datetime.now()
    content: str

    class Settings:
        name = "episodes"
        indexes = [
            IndexModel([("epi_title", ASCENDING)])
        ]

    class Config:
        schema_extra = {
            "example": {
                "epi_title": "The dark chambers of abyss",
                "season": "1",
                "epi_number": 1,
                "created": datetime.now(),
                "content": "file"
            }
        }


class EpisodeUpdate(BaseModel):
    anime_title: Optional[str]
    season: Optional[int]
    epi_number: Optional[int]
    content: Optional[str]
