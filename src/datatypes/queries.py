from enum import Enum


class Queries(str, Enum):
    FIRST = """
        SELECT url, url_host_name, warc_filename
        FROM ccindex.ccindex
        WHERE url_host_name = 'ulb.be'
        LIMIT 10
        """

    BASE_TYPO = """
        SELECT url_host_tld, url_host_2nd_last_part
        FROM ccindex.ccindex
        WHERE url_host_tld = %(1)s
        and url_host_2nd_last_part like %(2)s
        and crawl = %(3)s
        GROUP BY url_host_2nd_last_part, url_host_tld
        LIMIT 1000
        """
