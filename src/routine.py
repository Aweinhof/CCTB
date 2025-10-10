from src.query import Query
from pathlib import Path
import re
import time


def routine_check():
    """
    This is called at each execution of the script to check if we need to update the latest cc dataset name.
    The data is stored in '.store/current_crawl'.
    The request to the CC API is done if the file wasn't updated in the 24h.
    The directory and file is automaticaly created if it doesn't exist.
    A user shouldn't ever have to interact with this file.
    """
    fn = ".store/current_crawl"
    create_path(fn)

    with open(fn, 'r+') as f:
        content = f.read()
        fields = content.strip().split('\n')
        corrupt_msg = '[Warning] : .store/current_crawl file is corrupted or doesn\'t exist yet. Wiping it and rewriting it...'

        # case file is corrupted
        if len(fields) < 2 or not check_crawl_name_format(fields[0]) or not check_time_format(fields[1]):
            print(corrupt_msg)
            update_file(f)

        # case file is correct
        else:
            last_update_time = int(fields[1])
            seconds_24h = 60 * 60 * 24
            current = int(time.time())

            # case we didn't check for more than 24h
            if last_update_time + seconds_24h < current:
                print('Running daily check for latest CC name...')
                update_file(f)


def create_path(path: str):
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.touch(exist_ok=True)


def check_crawl_name_format(name):
    return bool(re.fullmatch(r'CC-MAIN-\d{4}-\d{2}', name))


def check_time_format(time_val):
    # funfact: this line will crash in year 2286
    return bool(re.fullmatch(r'\d{10}', time_val))


def update_file(f):
    """
    Fetches the latest CC dataset name from https://index.commoncrawl.org/collinfo.json
    checks the format of the returned value then stores it with the current time in sec since epoch
    """
    cc_name = Query.crawl_sets()[0]['id']
    current_time = int(time.time())

    if not check_crawl_name_format(cc_name):
        print("[Error] : latest crawl name returned by server seems wrong. Continuing without changing the "
              ".store/current_crawl file. If you want to continue using this tool make sure the first line "
              "of that file is the latest crawl name (ex: CC-MAIN-2025-38) or just fix me :) (update_file in src/routine.py")

    f.seek(0)
    f.truncate()
    f.write(cc_name + '\n' + str(current_time))
