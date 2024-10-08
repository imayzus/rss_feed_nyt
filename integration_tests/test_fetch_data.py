import api_router
import unittest
from ddt import data, ddt, unpack
from log import default_logger

logger = default_logger(__name__)


@ddt
class TestFetchData(unittest.TestCase):
    def setUp(self):
        pass

    @data(
        ("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",)
    )
    @unpack
    def test_fetch_feed_data(self, url):
        result = api_router.fetch_feed_data(url=url)
        assert len(result) > 0
        logger.debug(result[:1])
