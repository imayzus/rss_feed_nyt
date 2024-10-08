import unittest
from ddt import data, ddt, unpack
import utils
from log import default_logger

logger = default_logger(__name__)


@ddt
class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    @data(
        ('Tue, 01 Oct 2024 18:11:43 +0000', 'Oct. 01, 2024')
    )
    @unpack
    def test_get_short_date(self, published_date, expected):
        result = utils.get_short_date(published_date)
        logger.debug(f"result={result}")
        assert result == expected
