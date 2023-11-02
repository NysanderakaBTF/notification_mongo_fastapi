from fastapi import FastAPI

from api.notifications import notif_router

app = FastAPI()
app.include_router(notif_router)