from src.query import Query
from src.datatypes.filter import Filter


class CCTB:
    crawl_sets = []

    def __init__(self):
        self.crawl_sets = Query.crawl_sets()

    def get_indexes_filtered(self, url_pattern: str, contain: list, exact: list, regex: list, not_contain: list, not_exact: list, not_regex: list):
        contain = [Filter.CONTAIN(i) for i in contain]
        exact = [Filter.EXACT(i) for i in exact]
        regex = [Filter.REGEX(i) for i in regex]
        not_contain = [Filter.NOT_CONTAIN(i) for i in not_contain]
        not_exact = [Filter.NOT_EXACT(i) for i in not_exact]
        not_regex = [Filter.NOT_REGEX(i) for i in not_regex]

        return Query.filtered_indexes(self.crawl_sets[0], url_pattern,
                                      *contain,
                                      *exact,
                                      *regex,
                                      *not_contain,
                                      *not_exact,
                                      *not_regex)
