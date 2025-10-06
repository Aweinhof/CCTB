import argparse
import json


def build_parser():
    p = argparse.ArgumentParser(
        prog="parser.py",
        description="CTI tool leveraging common crawl database"
    )

    subparsers = p.add_subparsers(dest="command", required=True, help="Subcommands")

    # ------------------------------------ find ---------------------------------------

    # example index for ulb.be
    example = json.loads("{'urlkey': 'be,ulb)/', 'timestamp': '20250905152100', 'url': 'https://www.ulb.be/', 'mime': 'text/html', 'mime-detected': 'application/xhtml+xml', 'status': '200', 'digest': 'XGOGVKXIBKJVDQIV7CSQARVOCFXL4TOM', 'length': '30207', 'offset': '925416417', 'filename': 'crawl-data/CC-MAIN-2025-38/segments/1757047532686.9/warc/CC-MAIN-20250905142911-20250905172911-00434.warc.gz', 'languages': 'fra,eng', 'encoding': 'UTF-8'}".replace("'", '"'))
    additional_info = "Note :\n  Each of these arguments can be used multiple times in order to get more precise" \
                      "\n\nExample of index you can filter on :\n" + json.dumps(example, indent=4)

    find_p = subparsers.add_parser("find",
                                   help="Find a domain pattern with filters applied",
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog=additional_info)

    find_p.add_argument("host",
                        help="can be a pattern of a hostname or URL (ex : *.google.com)")

    find_p.add_argument("--typo-fuzz", action="store_true", help="Fuzz look alike characters to bust typosquatting")

    find_p.add_argument("--contain",
                        help="Contain string filter, EX : --contain languages:eng",
                        action="append",
                        default=[])
    find_p.add_argument("--exact",
                        help="Exact match string filter",
                        action="append",
                        default=[])
    find_p.add_argument("--regex",
                        help="Match regex filter",
                        action="append",
                        default=[])
    find_p.add_argument("--not-contain",
                        help="Doesn't Contain string filter",
                        action="append",
                        default=[])
    find_p.add_argument("--not-exact",
                        help="Is not string filter",
                        action="append",
                        default=[])
    find_p.add_argument("--not-regex",
                        help="Doesn't match regex filter",
                        action="append",
                        default=[])

    # ------------------------------------ chunks -------------------------------------

    chunks_p = subparsers.add_parser("chunks", help="Parses a chunks index file to show stats of it")

    chunks_p.add_argument("chunks_file", help="File containing the list of chunks")

    # ----------------------------------- find_page -----------------------------------

    find_page_p = subparsers.add_parser("find_page", help="Find a regex match in the content of the webpages")

    find_page_p.add_argument("regex", help="The regex to match a page")

    # -------------------------------------- dev --------------------------------------

    dev_p = subparsers.add_parser("dev", help="Developement branch")

    # dev_p.add_argument("regex", help="The regex to match a page")

    return p
