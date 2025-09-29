import requests
import json
from src.datatypes.filter import FilterValue


class Query:

    @staticmethod
    def crawl_sets() -> list[dict]:
        try:
            index_url = "https://index.commoncrawl.org/collinfo.json"
            indexes = json.loads(requests.get(index_url).text)
            return indexes

        except Exception:
            exit('Error: Connection refused')

    @staticmethod
    def filtered_indexes(crawlset: dict, url_pattern: str, *filters: FilterValue) -> list:
        index_server = crawlset['cdx-api']
        filters_url = "&".join([f.text for f in filters])
        URL = f'{index_server}?url={url_pattern}&{filters_url}&output=json'
        print(URL, '\n')
        response = requests.get(URL).text
        indexes = response.split('\n')
        indexes = indexes[:-1] if not indexes[-1] else indexes
        indexes = [json.loads(index) for index in indexes]
        return indexes
