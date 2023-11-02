import uvicorn

from core.config.env_config import config

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=config.APP_PORT, reload=True)