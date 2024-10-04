# from flask import Flask, jsonify
# from werkzeug.exceptions import HTTPException
# import feedparser
import fastapi
import uvicorn
import api_router
from utils import get_current_host, get_current_port


def create_app():
    # app = Flask(__name__)
    app = fastapi.FastAPI()
    app.include_router(api_router.router)
    return app


# @app.route('/', methods=['GET'])
# def index():
#     rss_news_urls = ["https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"]
#     data = []
#     for url in rss_news_urls:
#         data.append(feedparser.parse(url)['entries'])
#
#     return render_template('index.html', articles_data=data)


app = create_app()

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False)
    uvicorn.run('app:app', host='0.0.0.0', port=get_current_port(), reload=True)
