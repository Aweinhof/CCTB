import requests
import json
from src.datatypes.filter import FilterValue
from pyathena import connect
import pandas as pd
import warnings


class Query:

    @staticmethod
    def crawl_sets() -> list[dict]:
        try:
            index_url = "https://index.commoncrawl.org/collinfo.json"
            indexes = json.loads(requests.get(index_url, headers={'user-agent': 'cc-power-user/1.0'}).text)
            return indexes

        except Exception:
            exit('Error: Connection refused')

    @staticmethod
    def filtered_indexes(crawlset: dict, url_pattern: str, *filters: FilterValue) -> list:
        index_server = crawlset['cdx-api']
        filters_url = "&".join([f.text for f in filters])
        URL = f'{index_server}?url={url_pattern}&{filters_url}&output=json'
        print(URL, '\n')
        response = requests.get(URL, headers={'user-agent': 'cc-power-user/1.0'}).text
        indexes = response.split('\n')
        indexes = indexes[:-1] if not indexes[-1] else indexes
        indexes = [json.loads(index) for index in indexes]
        return indexes

    @staticmethod
    def contact_bucket():
        warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

        conn = connect(s3_staging_dir='s3://digit-cc-athena-query-results/',
                       region_name='us-east-1',
                       schema_name='ccindex')

        sql = """
        SELECT url, url_host_name, warc_filename
        FROM ccindex.ccindex
        WHERE url_host_name = 'ulb.be'
        LIMIT 1
        """

        df = pd.read_sql(sql, conn)
        print(df.head())
