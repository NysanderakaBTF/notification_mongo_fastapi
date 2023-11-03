from bson import ObjectId
from fastapi import HTTPException

from core.config.db_config import user_collection
from core.heplers.email_service import EmailService


class UserService:
    @staticmethod
    async def create_user(email: str, user_id: str | None = None):
        """
        Create a new user, if the user with given email/id already exists, raises HTTPException
        :param email: - email of created user
        :param user_id: - id of created, optional
        """
        email = EmailService.check_email(email)

        user = await user_collection.find_one({"email": email})
        if user:
            raise HTTPException(400, "User with this email already exists")
        if not email:
            raise HTTPException(400, "No email")
        data = {"email": email, "notifications": []}
        if user_id:
            num_with_id = await user_collection.count_documents({"_id": user_id})
            if num_with_id:
                raise HTTPException(400, "User with such id already exists")
            data["_id"] = ObjectId(user_id)
        return await user_collection.insert_one(data)

    @staticmethod
    async def get_user(user_id: str):
        """Returns a user by id"""
        return await user_collection.find_one({"_id": user_id})
