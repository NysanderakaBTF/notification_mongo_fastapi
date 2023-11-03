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

