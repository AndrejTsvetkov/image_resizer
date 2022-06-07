import uvicorn
from fastapi import FastAPI

from app.routers import router

app = FastAPI()

app.include_router(router)


if __name__ == '__main__':  # pragma: no cover (for debug purposes)
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
