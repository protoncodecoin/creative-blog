from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .db import database

from app.routers.post import article_route
from app.routers.publisher import publisher_route
from app.routers.anime import anime_router
from app.routers.episode import episode_router

app = FastAPI()

database = database.Settings()


app.include_router(article_route, prefix="/articles", tags=["articles"])
app.include_router(publisher_route, prefix="/publisher", tags=["publisher"])
app.include_router(anime_router, prefix="/anime", tags=["anime"])
app.include_router(episode_router, prefix="/episode", tags=["episode"])


@app.on_event("startup")
async def start_db():
    await database.init_db()


@app.get("/")
def index() -> HTMLResponse:
    html_content = """
   <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <h1>Welcome to the Creative Blog</h1>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

