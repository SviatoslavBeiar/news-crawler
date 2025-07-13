# api.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional

from models import SessionLocal, Article

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/articles", response_model=List[dict])
async def get_articles(
    category: Optional[str] = None,
    sentiment: Optional[str] = None,
    limit: int = 100
):
    session = SessionLocal()
    query = session.query(Article)
    if category:
        query = query.filter_by(category=category)
    if sentiment:
        query = query.filter_by(sentiment=sentiment)
    results = (
        query
        .order_by(Article.published_at.desc())
        .limit(limit)
        .all()
    )
    session.close()
    return [
        {
            "id": a.id,
            "title": a.title,
            "url": a.url,
            "published_at": a.published_at,
            "category": a.category,
            "sentiment": a.sentiment
        }
        for a in results
    ]



@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    session = SessionLocal()
    art = session.query(Article).get(article_id)
    session.close()
    if not art:
        raise HTTPException(status_code=404, detail="Article not found")
    return {
        "id": art.id,
        "title": art.title,
        "url": art.url,
        "published_at": art.published_at,
        "content": art.content,
        "category": art.category,
        "sentiment": art.sentiment
    }
