import requests
import json
from src.datatypes.filter import FilterValue
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor
import boto3
from pathlib import Path
from src.logger import log


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
        log(URL + '\n')
        response = requests.get(URL, headers={'user-agent': 'cc-power-user/1.0'}).text
        indexes = response.split('\n')
        indexes = indexes[:-1] if not indexes[-1] else indexes
        indexes = [json.loads(index) for index in indexes]
        return indexes

    @staticmethod
    def athena(query, values):
        conn = connect(s3_staging_dir='s3://digit-cc-athena-query-results/',
                       region_name='us-east-1',
                       schema_name='ccindex')
        cursor = conn.cursor(PandasCursor)

        params = {}
        for i in range(len(values)):
            params[str(i + 1)] = values[i]

        df = cursor.execute(query, params).fetchall()
        scanned_bytes = cursor.data_scanned_in_bytes or 0
        # TODO : make a cast to MB GB TB
        log(f"Data scanned: {scanned_bytes / 1e6:.2f} MB")

    @staticmethod
    def fetch_chunks_indexes(id):
        Path('chunklist').mkdir(parents=True, exist_ok=True)

        s3 = boto3.client('s3')
        bucket = 'commoncrawl'
        prefix = f'crawl-data/{id}/segments/'

        warc_files = []

        paginator = s3.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

        for page in page_iterator:
            for obj in page.get('Contents', []):
                key = obj['Key']
                if key.endswith('.warc.gz'):
                    warc_files.append(key)

        with open('chunklist/' + id, 'w') as f:
            for line in warc_files:
                f.write(line + '\n')
