from fastapi import APIRouter, status, Request
from starlette.templating import Jinja2Templates
import feedparser
import cachetools.func
from typing import Optional
import utils
from utils import (get_cache_ttl_minutes, get_short_date, get_current_date,
                   get_base_url, get_result_data)
from log import default_logger
from models import Result


logger = default_logger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@cachetools.func.ttl_cache(maxsize=None, ttl=get_cache_ttl_minutes() * 60)
def fetch_feed_data(url: str) -> list:
    logger.info("getting data from feedparser")
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

    # switch to use_ssl=True to use https://localhost:port or leave as False to use http://
    return templates.TemplateResponse(request, name='index.html',
                                      context={'articles_data': data, 'current_date': get_current_date(),
                                               'language': language, 'base_url': get_base_url(use_ssl=False)})


@router.get('/result', status_code=status.HTTP_200_OK)
def fetch_genes_result(request: Request):
    data = get_result_data()
    result = Result(result=data)
    result_by_category = utils.break_into_categories(result.result)
    utils.sort_four_categories(result_by_category)
    return result_by_category
