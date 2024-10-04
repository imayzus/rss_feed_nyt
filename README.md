This is a demo implementation of displaying NY Times RSS feed https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml
To run:
1. create virtual environment and install dependencies using requirements.txt
2. edit config.json to set desired port, which by default is set to 5000
3. run python app.py
This will start uvicorn server on localhost:5000. 
4. Access the page in http://localhost:5000
The main page takes a parameter language, which switches the bold decoration between ENG and ESP in the head, e.g.
http://localhost:5000?language=ENG 
http://localhost:5000?language=ESP

This implementation caches the feed for 15 minutes, which is also configured in config.json.