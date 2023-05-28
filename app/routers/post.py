from fastapi import APIRouter, status, HTTPException, Depends
from ..db.database import QueryDatabase
from ..models.post import Article, ArticleUpdate
from ..models.publisher import Publisher

from ..auth.authenticate import get_current_user


from typing import List

from beanie import PydanticObjectId

article_route = APIRouter(tags=["posts"])

post_database = QueryDatabase(Article)
episodes_database = QueryDatabase(Publisher)


@article_route.get("/all")
async def get_articles() -> List[Article]:
    """ Retrieve all Articles"""
    articles = await post_database.get_all()
    if not articles:
        return []
    return articles


@article_route.get("/{id}", response_model=Article, status_code=200)
async def get_article(id: PydanticObjectId):
    """ Get Article by specified id"""
    article = await post_database.get_by_id(id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id '{id}' not found"
        )
    return article


@article_route.post("/create", status_code=201)
async def create_article(payload: Article):
    """ Create Article"""
    # if current_publisher.email:
    #     payload.publisher = current_publisher
    await post_database.save(payload)
    return {
        "message": "Series Created Successfully"
    }


@article_route.put("/update/{id}", response_model=Article, status_code=200)
async def update_article(id: PydanticObjectId, payload: ArticleUpdate):
    """ Update a specific article by providing the ID"""
    article_update = await post_database.update(id, payload)
    if not article_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id '{id}' not found"
        )
    return article_update

