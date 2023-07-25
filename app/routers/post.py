from fastapi import APIRouter, status, HTTPException, Depends
from ..db.database import QueryDatabase
from ..models.post import Article, ArticleUpdate, ArticleResponse
from ..models.publisher import Publisher, UserResponse
from ..models.token import TokenData

from ..auth.authenticate import get_current_user


from typing import List

from beanie import PydanticObjectId

article_route = APIRouter(tags=["posts"])

post_database = QueryDatabase(Article)
publisher_db = QueryDatabase(Publisher)


@article_route.get("/all", response_model=List[ArticleResponse])
async def get_articles():
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
async def create_article(payload: Article, current_publisher: TokenData = Depends(get_current_user)):
    """ Create Article"""
    publisher = await publisher_db.get_user_by_email(current_publisher.email)
    payload.publisher = publisher
    await post_database.save(payload)
    return {
        "message": "Series Created Successfully"
    }


@article_route.put("/update/{id}", response_model=Article, status_code=200)
async def update_article(id: PydanticObjectId, payload: ArticleUpdate,
                         current_publisher: TokenData = Depends(get_current_user)):
    """ Update a specific article by providing the ID"""
    existing_article = await post_database.get_by_id(id)
    if not existing_article.publisher.email == current_publisher.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid publisher credentials to perform requested action"
        )
    article_update = await post_database.update(id, payload)
    if not article_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with id '{id}' not found"
        )
    return article_update


@article_route.delete("/delete/all")
async def delete_all_articles(current_publisher: TokenData = Depends(get_current_user)):
    """Delete all articles from the db"""
    # get all posts for publisher
    publisher = await publisher_db.get_user_by_email(current_publisher.email)
    if not publisher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized for this action"
        )
    await post_database.delete_all_publisher_posts(current_publisher.email)

    # posts = await post_database.get_all()
    # await post_database.delete_all()
    return {
        "message": f"Articles deleted for publisher {publisher.username}"
    }


@article_route.delete("/delete/{id}")
async def delete_article(id: PydanticObjectId):
    """ Delete an article with the specified id"""
    article = await post_database.get_by_id(id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with the specified id {id} not found"
        )
    await post_database.delete(id)
    return {
        "message": "Article was deleted"
    }
