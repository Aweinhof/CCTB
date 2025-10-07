from pathlib import Path
from src.query import Query
import gzip
import requests
import time


class ChunksParser:
    result = {}
    warc_type = 0
    robotstxt_type = 0
    crawldiagnostics_type = 0

    def __init__(self, dataset_id):
        Path('chunklist').mkdir(parents=True, exist_ok=True)
        path = Path('chunklist/' + dataset_id)

        if not path.exists():
            try:
                input('Index file for this dataset doesn\'t exist yet. Press enter if you want to download it (~35Mb)')
                Query.fetch_chunks_indexes(dataset_id)
            except Exception as e:
                print("Error, probably invalid authentication token : ")
                print(e)

        with open(path, 'r') as f:
            self.treat_chunks_file(f)

    def rec_stats(self, type_str):
        match type_str:
            case "warc":
                self.warc_type += 1
            case "robotstxt":
                self.robotstxt_type += 1
            case "crawldiagnostics":
                self.crawldiagnostics_type += 1
            case _:
                print("WARNING : unknown file type found : " + type_str)

    def treat_chunks_file(self, f):
        while line := f.readline():
            line = line.strip()
            splitted = line.split('-')
            splitted[-1] = "xxxxx.warc.gz"
            self.rec_stats(splitted[-5].split('/')[-2])
            line = "-".join(splitted)
            self.add_to_dict(line)

    def add_to_dict(self, line):
        if line in self.result:
            self.result[line] += 1
        else:
            self.result[line] = 1

    def print(self):
        biggest = 0
        amount_width = 8

        for key in self.result:
            if len(key) > biggest:
                biggest = len(key)

        print('+ ' + (biggest + 2) * '-' + '+' + amount_width * '-' + '+')
        print('| ' + (biggest + 2) * ' ' + '|' + amount_width * ' ' + '|')

        for key in self.result:
            amount = str(self.result[key])
            padding = biggest - len(key)
            print('|  ' + key + padding * ' ' + ' | ' + amount + (amount_width - 2 - len(amount)) * ' ' + ' |')

        print('| ' + (biggest + 2) * ' ' + '|' + amount_width * ' ' + '|')
        print('+ ' + (biggest + 2) * '-' + '+' + amount_width * '-' + '+')

        print('| ' + (biggest + 2) * ' ' + '|' + amount_width * ' ' + '|')

        # crawl type
        amount = str(self.warc_type)
        key = "Total # warc type"
        padding = biggest - len(key)
        print('|  ' + key + padding * ' ' + ' | ' + amount + (amount_width - 2 - len(amount)) * ' ' + ' |')

        # robotstxt type
        amount = str(self.robotstxt_type)
        key = "Total # robotstxt type"
        padding = biggest - len(key)
        print('|  ' + key + padding * ' ' + ' | ' + amount + (amount_width - 2 - len(amount)) * ' ' + ' |')

        # crawldiagnostics type
        amount = str(self.crawldiagnostics_type)
        key = "Total # crawldiagnostics type"
        padding = biggest - len(key)
        print('|  ' + key + padding * ' ' + ' | ' + amount + (amount_width - 2 - len(amount)) * ' ' + ' |')

        print('| ' + (biggest + 2) * ' ' + '|' + amount_width * ' ' + '|')
        print('+ ' + (biggest + 2) * '-' + '+' + amount_width * '-' + '+')
