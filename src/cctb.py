from src.query import Query
from src.datatypes.queries import Queries
from src.datatypes.filter import Filter
from src.chunk_scanner import ChunkScanner
import config
from src.logger import error


class CCTB:
    crawl_sets = []

    def __init__(self):
        pass

    def get_indexes_filtered(self,
                             url_pattern: str,
                             contain: list = [],
                             exact: list = [],
                             regex: list = [],
                             not_contain: list = [],
                             not_exact: list = [],
                             not_regex: list = []):
        contain = [Filter.CONTAIN(i) for i in contain]
        exact = [Filter.EXACT(i) for i in exact]
        regex = [Filter.REGEX(i) for i in regex]
        not_contain = [Filter.NOT_CONTAIN(i) for i in not_contain]
        not_exact = [Filter.NOT_EXACT(i) for i in not_exact]
        not_regex = [Filter.NOT_REGEX(i) for i in not_regex]

        if not self.crawl_sets:
            self.crawl_sets = Query.crawl_sets()

        return Query.filtered_indexes(self.crawl_sets[0], url_pattern,
                                      *contain,
                                      *exact,
                                      *regex,
                                      *not_contain,
                                      *not_exact,
                                      *not_regex)

    def scan_chunk(self, path):
        scanner = ChunkScanner()
        scanner.scan(path)

    def phishing(self, auto, hostname):
        if auto:
            print("Work in progress")
            return

        splitted = hostname.split('.')
        if len(splitted) != 2 or not splitted[0] or not splitted[1]:
            error("Invalid hostname given, see -h for more info")
            return

        params = splitted + [config.latest_cc]
        Query.athena(Queries.BASE_TYPO, params)
