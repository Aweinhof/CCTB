import boto3

s3 = boto3.client('s3')
bucket = 'commoncrawl'
prefix = 'crawl-data/CC-MAIN-2018-17/segments/'

warc_files = []

paginator = s3.get_paginator('list_objects_v2')
page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

for page in page_iterator:
    for obj in page.get('Contents', []):
        key = obj['Key']
        if key.endswith('.warc.gz'):
            warc_files.append(key)

print(f"Found {len(warc_files)} WARC files in CC-MAIN-2018-17:")
for f in warc_files:
    print(f)
