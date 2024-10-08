from datetime import datetime
import json
import models

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


def get_result_data():
    with open('genes.json', 'r') as f_in:
        data = json.load(f_in)
        return data

"""
create a data model class for the data
create a GET endpoint “/result” with sorted data returned in the following 4 categories in the order specified and each category sorted per sub bullet point
genes with high risk
same category, count the number of high risk conditions from high to low
genes with high risk and inconclusive
same category, count the number of high risk conditions from high to low
genes with inconclusive but no high risk
same category, count the number of inconclusive conditions from high to low
genes with low risk only
same category, count the number of low risk conditions from high to low
although the data is small example, the code logic should work with arbitrary number of genes and arbitrary number of conditions
"""
def break_into_categories(genes: list[models.Gene]):
    high_no_inconclusive = []
    high_with_inconclusive = []
    low_with_inconclusive = []
    low_no_inconclusive = []
    for gene in genes:
        number_high_risk = sum([1 for cat in gene.riskCategories if cat.risk == 'high'])
        number_inconclusive = sum([1 for cat in gene.riskCategories if cat.risk == 'inconclusive'])
        number_low = sum([1 for cat in gene.riskCategories if cat.risk == 'low'])
        gene.number_high_risk = number_high_risk
        gene.number_inconclusive = number_inconclusive
        gene.number_low = number_low
        if number_high_risk > 0:
            if number_inconclusive > 0:
                high_with_inconclusive.append(gene)
            else:
                high_no_inconclusive.append(gene)
        else:
            if number_inconclusive > 0:
                low_with_inconclusive.append(gene)
            else:
                low_no_inconclusive.append(gene)

    res = models.SortedResult(high_no_inconclusive=high_no_inconclusive,
                              high_with_inconclusive=high_with_inconclusive,
                              low_with_inconclusive=low_with_inconclusive,
                              low_no_inconclusive=low_no_inconclusive)
    return res


def sort_four_categories(sorted_result: models.SortedResult):
    sorted_result.high_no_inconclusive.sort(key=lambda g: g.number_high_risk, reverse=True)
    sorted_result.high_with_inconclusive.sort(key=lambda g: g.number_inconclusive)
    sorted_result.low_with_inconclusive.sort(key=lambda g: g.number_inconclusive)
    sorted_result.low_no_inconclusive.sort(key=lambda g: g.number_low)
