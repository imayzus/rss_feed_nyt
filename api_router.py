from fastapi import APIRouter, status, Request
# from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import feedparser
# from functools import lru_cache
import cachetools.func
import logging
from typing import Optional
from utils import get_cache_ttl_minutes, get_short_date, get_current_date, get_base_url


logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@cachetools.func.ttl_cache(maxsize=None, ttl=get_cache_ttl_minutes() * 60)
def fetch_feed_data(url: str) -> list:
    print("getting data from feedparser")
    return feedparser.parse(url)['entries']


@router.get('/', status_code=status.HTTP_200_OK)
def index(request: Request, language: Optional[str] = 'ENG'):
    rss_news_urls = ["https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"]
    data = []
    for url in rss_news_urls:
        data.append(fetch_feed_data(url))

    for article in data[0]:
        if article.get('published'):
            article['published_date'] = get_short_date(article['published'])

    return templates.TemplateResponse(request, name='index.html',
                                      context={'articles_data': data, 'current_date': get_current_date(),
                                               'language': language, 'base_url': get_base_url()})
