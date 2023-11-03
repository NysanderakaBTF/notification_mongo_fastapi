from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException

from app.notifications.schemas.notofication import CreateNotificationRequest
from core.config.db_config import user_collection


class NotificationService:

    @staticmethod
    async def create_notification(notification: CreateNotificationRequest):
        """
        Creates a notification for user, if no such user or limit on notification reached,
        produces HTTPException
        :param notification: schema of notification to create
        :return: result of creation of notification and user's email
        """
        user = await user_collection.find_one({"_id": ObjectId(notification.user_id)})
        if not user:
            raise HTTPException(404, detail="User not found")
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
        return {"res": res, "email": user['email']}

    @staticmethod
    async def get_list(user_id: str, skip=0, limit=10):
        """
        Returns a list of notifications for a given user according to pagination params
        :param user_id: id of the user to get notifications from
        :param skip: how many notifications to skip
        :param limit: How many notifications to return
        """
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
            {"$limit": limit},
            {"$unset": "_id"}
        ]).to_list(limit)

    @staticmethod
    async def mark_as_read(notification_id: str):
        """
        Mark a notification as read, if no such notification with given id raises HTTPException
        :param notification_id: id of notification to mark as read
        """
        res = await user_collection.find_one({"notifications._id": ObjectId(notification_id)})
        if not res:
            raise HTTPException(404, detail="No such notification fot id")
        return await user_collection.update_one({"notifications._id": ObjectId(notification_id)}, {
            "$set": {"notifications.$.is_new": False}
        })

    @staticmethod
    async def count_all_and_new(user_id: str):
        """
        Gives a number of notifications for user and a a number of unread notifications
        :param user_id: id of the user
        """
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
