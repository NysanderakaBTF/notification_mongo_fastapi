import json
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.notifications.schemas.notofication import CreateNotificationRequest
from app.notifications.service.notififcation import NotificationService
from app.notifications.service.user import UserService
from core.heplers.email_service import EmailService
notif_router = APIRouter(tags=["Notifications"])


@notif_router.post("/create")
async def create(notif_schema: CreateNotificationRequest, email: str | None = None):
    """
    Creates a email/user and sends it according to the key in notif_schema.
    key - registration - sends email, adds user
        - "new_message", "new_post" - creates a notification
        - "new_login" - creates a notification and sends email to user's email
    :param notif_schema: CreateNotificationRequest - schema of created notification
    :param email: email of user, used in registration scenario
    """
    try:
        if notif_schema.key == "registration":
            res = await UserService.create_user(email, notif_schema.user_id)
            await EmailService.send_email("user created", email)
            return JSONResponse(status_code=201, content={'success': True})
        if notif_schema.key in ["new_message", "new_post"]:
            await NotificationService.create_notification(notif_schema)
            return JSONResponse(status_code=201, content={'success': True})
        if notif_schema.key == "new_login":
            res = await NotificationService.create_notification(notif_schema)
            await EmailService.send_email(notif_schema.key, res['email'])
            return JSONResponse(status_code=201, content={'success': True})
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@notif_router.get('/list')
async def get_list(user_id: str, skip: int = 0, limit: int = 10):
    """
    Used to get a list of user's notifications with number of read/total
    :param user_id: id of user to get information about
    :param skip: number of skipped notifications in returned list
    :param limit: max number of notifications in returned list
    """
    if not user_id:
        raise HTTPException(400, detail="user_id must be specified")

    stat = await NotificationService.count_all_and_new(user_id)
    list_ = await NotificationService.get_list(user_id, skip, limit)

    return JSONResponse(status_code=200, content={
        "success": True,
        "data": {
            "elements": stat['total'],
            "new": stat['new'],
            "request": {
                "user_id": user_id,
                "skip": skip,
                "limit": limit
            },
            "list": json.loads(json.dumps(list_, default=str))
        }
    })


@notif_router.post('/read')
async def read(user_id: str, notification_id: str):
    """
    Used to mark notifications as read
    :param user_id: user's ID
    :param notification_id: id of notification that will be marked as read
    """
    try:
        await NotificationService.mark_as_read(notification_id)
        return JSONResponse(status_code=200, content={"success": True})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"success": False, "error": e})
