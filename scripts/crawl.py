import requests
import json
import sys
import gzip
import io
from urllib.parse import quote_plus

# The URL of the Common Crawl Index server
SERVER = 'http://index.commoncrawl.org/'
INDEX_NAME = 'CC-MAIN-2025-38'

target_url = sys.argv[1] if len(sys.argv) > 1 else 'ulb.be'
myagent = 'cc-get-started/1.0 (Example data retrieval script; yourname@example.com)'


def search_cc_index(url):
    encoded_url = quote_plus(url)
    index_url = f'{SERVER}{INDEX_NAME}-index?url={encoded_url}&output=json'
    response = requests.get(index_url, headers={'user-agent': myagent})

    if response.status_code == 200:
        records = response.text.strip().split('\n')
        return [json.loads(record) for record in records]
    else:
        return None


def fetch_record(record):
    offset, length = int(record['offset']), int(record['length'])
    s3_url = f'https://data.commoncrawl.org/{record["filename"]}'

    # Define the byte range for the request
    byte_range = f'bytes={offset}-{offset + length - 1}'

    # Send the HTTP GET request to the S3 URL with the specified byte range
    response = requests.get(
        s3_url,
        headers={'user-agent': myagent, 'Range': byte_range},
        stream=True
    )

    with open('output.warc', 'wb') as out:
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
            data = f.read()
            out.write(data)


def str_time(timestamp):
    year = timestamp[0:4]
    month = timestamp[4:6]
    day = timestamp[6:8]
    return day + '/' + month + '/' + year


records = search_cc_index(target_url)
if records:
    print(f"Found {len(records)} records for {target_url}")
    for i in range(len(records)):
        record = records[i]
        print(str(i) + ' ---> URL : ' + record['url'] + ' Date : ' + str_time(record['timestamp']) + ', Size : ' + record['length'] + ', Status : ' + record['status'])

    usr_input = input('Select number to request : ')
    print('=' * 30)
    print(records[int(usr_input)])
    print('=' * 30)
    input('Press any key to download response...')
    fetch_record(records[int(usr_input)])

else:
    print(f"No records found for {target_url}")
