from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class NotificationKey(str, Enum):
    registration = 'registration'
    new_message = 'new_message'
    new_post = 'new_post'
    new_login = 'new_login'


class CreateNotificationRequest(BaseModel):
    user_id: str = Field(..., description="ОbjectID документа пользователя которому отправляется уведомление")
    target_id: Optional[str] = Field(description="ObjectID документа сущности, к которой относится уведомление", default=None)
    key: NotificationKey = Field(..., description="ключ уведомления enum")
    data: Optional[dict] = Field(description="произвольный объект из пар ключ/значение", default={})


class CreateNotificationResponse(BaseModel):
    success: bool = Field(..., description="Статус выполнения запроса")


class GetNotificationResponse(CreateNotificationRequest):
    id: str = Field(..., description="If of notification", alias="_id")
    timestamp: int = Field(..., description="Creation timestamp")
    is_new: bool = Field(..., description="Flag indicating whether notification was read")
