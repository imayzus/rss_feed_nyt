from datetime import datetime
import json

cached_config = {}


def get_config(location='config.json', ignore_cache=False) -> dict:
    if not cached_config or ignore_cache:
        with open(location, 'r') as f_in:
            config_json = json.load(f_in)
            cached_config['config'] = config_json
    return cached_config['config']


def get_cache_ttl_minutes() -> int:
    return get_config().get('cache_ttl_minutes')


def get_short_date(published_date: str) -> str:
    """ transform a string like 'Tue, 01 Oct 2024 18:11:43 +0000' into 'Oct. 01, 2024' """
    tokens = published_date.split()
    date_short_format = f"{tokens[2]}. {tokens[1]}, {tokens[3]}"
    return date_short_format


def get_current_date() -> str:
    """ return a date in the format Fri. 4 Oct 2024 """
    now = datetime.now()
    result = now.strftime("%a. %d %b %Y")
    return result


def get_current_host() -> str:
    return get_config()['host']


def get_current_port() -> int:
    return get_config()['port']


def get_base_url(use_ssl) -> str:
    return f'http://{get_current_host()}:{get_current_port()}' if not use_ssl else \
        f'https://{get_current_host()}:{get_current_port()}'
