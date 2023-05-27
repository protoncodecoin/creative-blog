from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from db import database

from api.endpoints.post import article_route
from api.endpoints.publisher import publisher_route

app = FastAPI()

database = database.Settings()


app.include_router(article_route, prefix="/articles")
app.include_router(publisher_route, prefix="/publisher")


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

