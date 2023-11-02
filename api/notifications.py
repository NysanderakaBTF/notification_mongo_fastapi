import json

from bson import json_util
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.notifications.schemas.notofication import CreateNotificationRequest, GetNotificationResponse
from app.notifications.service.notififcation import NotificationService
from app.notifications.service.user import UserService
from core.heplers.email_service import EmailService
from aiosmtplib.errors import SMTPException
from fastapi import Response

notif_router = APIRouter(tags=["Notifications"])


@notif_router.post("/create")
async def create(notif_schema: CreateNotificationRequest, email: str | None = None):
    if notif_schema.key == "registration":
        try:
            res = await UserService.create_user(email, notif_schema.user_id)
            user = await UserService.get_user(res.inserted_id)
            print(user)
            await EmailService.send_email("user created", user['email'])
            return JSONResponse(status_code=201, content={"success": True})
        except Exception as e:
            return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    if notif_schema.key in ["new_message", "new_post"]:
        try:
            await NotificationService.create_notification(notif_schema)
            return JSONResponse(status_code=201, content={'success': True})
        except Exception as e:
            return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

    if notif_schema.key == "new_login":
        try:
            res = await NotificationService.create_notification(notif_schema)
            await EmailService.send_email(notif_schema.key, res['email'])
            return JSONResponse(status_code=201, content={'success': True})
        except Exception as e:
            return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@notif_router.get('/list')
async def list(user_id: str, skip: int = 0, limit: int = 10):
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
    try:
        await NotificationService.mark_as_read(notification_id)
        return JSONResponse(status_code=200, content={"success":True})
    except Exception as e:
        raise HTTPException(status_code=400, detail={"success": False, "error": e})
