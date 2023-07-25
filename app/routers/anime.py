from fastapi import APIRouter
from ..models.anime import Anime, AnimeUpdate, AnimeResponse

from beanie import PydanticObjectId

from ..db.database import QueryDatabase

from typing import List

anime_router = APIRouter(tags=["anime"])


anime_db = QueryDatabase(Anime)


@anime_router.get("/all", response_model=List[Anime], status_code=200)
async def get_all_anime():
    """Get all the Anime"""
    all_animes = await anime_db.get_all()
    return all_animes


@anime_router.get("/{id}", response_model=AnimeResponse)
async def get_anime_by_id(id: PydanticObjectId):
    """Get Anime with the specified id"""
    anime = await anime_db.get_by_id(id)
    return anime


@anime_router.post("/create", status_code=201)
async def create_anime(payload: Anime):
    """Create anime """
    # new_anime = payload
    await anime_db.save(payload)
    return {
        "message": "Anime created"
    }


@anime_router.put("/update/{id}", response_model=AnimeResponse, status_code=200)
async def update_anime(id: PydanticObjectId, payload: AnimeUpdate):
    """ Update Anime"""
    updated_anime = await anime_db.update(id, payload)
    return updated_anime


@anime_router.delete("delete/{id}", status_code=200)
async def delete_anime(id: PydanticObjectId):
    """Delete Anime with the specified id"""
    await anime_db.delete(id)
    return {
        "message": "anime was deleted"
    }
