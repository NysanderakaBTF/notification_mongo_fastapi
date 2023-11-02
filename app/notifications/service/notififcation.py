from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException

from app.notifications.schemas.notofication import CreateNotificationRequest
from core.config.db_config import user_collection


class NotificationService:

    @staticmethod
    async def create_notification(notification: CreateNotificationRequest):
        user = await user_collection.find_one({"_id": ObjectId(notification.user_id)})
        if not user:
            raise HTTPException(404, detail="User not found")
        print(user)
        if len(user['notifications']) > 100:
            raise HTTPException(403, detail="Maximum number of notifications for "
                                            "user in reached")
        res = await user_collection.update_one({"_id": ObjectId(notification.user_id)},
                                               {'$push': {
                                                   "notifications": {
                                                       "timestamp": datetime.timestamp(datetime.now()),
                                                       "is_new": True,
                                                       "user_id": ObjectId(notification.user_id),
                                                       "key": notification.key,
                                                       "target_id": ObjectId(
                                                           notification.target_id) if notification.target_id else None,
                                                       "data": notification.data,
                                                       "_id": ObjectId()
                                                   }
                                               }}
                                               )
        print(res)
        return {"res": res, "email": user['email']}

    @staticmethod
    async def get_list(user_id: str, skip=0, limit=10):
        return await user_collection.aggregate([
            {"$match": {"notifications.user_id": ObjectId(user_id)}},
            {"$unwind": "$notifications"},
            {"$project": {
                "id": "$notifications._id",
                "timestamp": "$notifications.timestamp",
                "is_new": "$notifications.is_new",
                "user_id": "$notifications.user_id",
                "key": "$notifications.key",
                "target_id": "$notifications.target_id",
                "data": "$notifications.data"
            }},
            {"$skip": skip},
            {"$limit": limit}
        ]).to_list(limit)

    @staticmethod
    async def mark_as_read(notification_id: str):
        res = await user_collection.find_one({"notifications._id": ObjectId(notification_id)})
        if not res:
            raise HTTPException(404, detail="No such notification fot id")
        return await user_collection.update_one({"notifications._id": ObjectId(notification_id)}, {
            "$set": {"notifications.$.is_new": False}
        })

    @staticmethod
    async def count_all_and_new(user_id: str):
        return (await user_collection.aggregate([
            {"$match": {"notifications.user_id": ObjectId(user_id)}},
            {"$unwind": "$notifications"},
            {
                "$group": {
                    "_id": "$notifications.user_id",
                    "total": {"$sum": 1},
                    "new": {"$sum": {
                         "$cond": [
                             {"$eq": ["$notifications.is_new", True]}, 1, 0]
                    }}
                }
            },
        ]).to_list(1))[0]
