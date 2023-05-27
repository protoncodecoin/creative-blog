from beanie import Document
from datetime import datetime
from pymongo import IndexModel, DESCENDING
from pydantic import BaseModel

from models.publisher import Publisher

from typing import Optional


class Article(Document):
    title: str
    content: str
    image_url: Optional[str] = None
    created: Optional[datetime] = datetime.now()
    publisher: Publisher

    class Settings:
        name = "series"
        indexes = [
           IndexModel([("title", DESCENDING)])
        ]

    class Config:
        schema_extra = {
            "example": {
                "title": "Attack On Titans",
                "content": "A world dominated my giant flesh eating creatures",
                "image_url": "https://www.globephotography.com/kingfisher.jpg",
                "created": datetime.now(),
            }
        }


class ArticleUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    image_url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "The Old gods vd The new gods",
                "content": "This story tells the brutal battle that happened between the ....",
                "image_url": "https://www.legacystories.com/old-gods-vs-new-gods.jpg",
            }
        }
