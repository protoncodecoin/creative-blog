from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from pydantic import BaseModel, BaseSettings

from typing import Any, List, Optional

from models import post, publisher


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None
    ALGORITHM: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None

    async def init_db(self):
        client = AsyncIOMotorClient(
            self.DATABASE_URL
        )

        await init_beanie(database=client.db_name, document_models=[post.Article,
                                                                    publisher.Publisher])

    class Config:
        env_file = ".env"


class QueryDatabase:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        """ document :-> instance of the document passed to the DB"""
        await document.create()
        return

    async def get_by_id(self, id: PydanticObjectId) -> Any:
        document = await self.model.get(id)
        if document:
            return document
        return False

    async def get_all(self) -> List[Any]:
        """ Get all documents from the database"""
        documents = await self.model.find_all().to_list()
        return documents

    async def get_user_by_email(self, email):
        """ Get document by email"""
        document = await self.model.find_one(self.model.email == email)
        return document

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        """ Update document in the DB based on the supplied id"""
        document_id = id
        des_body = body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        updated_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        document = await self.get_by_id(document_id)
        if not document:
            return False
        await document.update(updated_query)
        return document

    async def delete(self, id: PydanticObjectId):
        """ Delete document from the DB using the supplied id"""
        document = await self.model.get(id)
        if not document:
            return False
        await document.delete()
        return True

    async def delete_all(self):
        """clear the database. Be careful with this method as it wipes the DB clean"""
        await self.model.find_all().delete()
        return True
