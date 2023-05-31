from fastapi import APIRouter, status

from beanie import PydanticObjectId

from ..models.anime import Episode, Anime
from ..db.database import QueryDatabase

episode_db = QueryDatabase(Episode)

episode_router = APIRouter(tags=["episodes"])


@episode_router.post("/create")
async def create_episode(payload: Episode):
    """Create or upload episode"""
    await episode_db.save(payload)
    return {
        "message": "created successfully"
    }


@episode_router.get("/all")
async def get_all_episodes():
    """ get all episodes """
    queried_episodes = await episode_db.get_all()
    return queried_episodes


@episode_router.put("/{id}")
async def update(id: PydanticObjectId, payload: Episode):
    """ update the episode with the specified id"""
    update_epi = payload
    await episode_db.update(id, update_epi)
    return update_epi


@episode_router.delete("/{id}")
async def delete_episode_by_id(id: PydanticObjectId):
    """ Delete episode with the specified id"""
    await episode_db.delete(id)
    return {
        "message": "Episode deleted successfully"
    }
