import argparse
import sys
from src.cctb import CCTB


def build_parser():
    p = argparse.ArgumentParser(
        prog="parser.py",
        description="Example CLI demonstrating positional args, flags, groups and subcommands."
    )

    p.add_argument("host",
                   help="can be a pattern of a hostname or URL (ex : *.google.com)")

    # These are all the filters you can apply on the indexing queries
    p.add_argument("--contain",
                   help="Contain string filter",
                   action="append",
                   default=[])
    p.add_argument("--exact",
                   help="Exact match string filter",
                   action="append",
                   default=[])
    p.add_argument("--regex",
                   help="Match regex filter",
                   action="append",
                   default=[])
    p.add_argument("--not-contain",
                   help="Doesn't Contain string filter",
                   action="append",
                   default=[])
    p.add_argument("--not-exact",
                   help="Is not string filter",
                   action="append",
                   default=[])
    p.add_argument("--not-regex",
                   help="Doesn't match regex filter",
                   action="append",
                   default=[])

    return p

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)
    cctb = CCTB()

    indexes = cctb.get_indexes_filtered(args.host,
                                        args.contain,
                                        args.exact,
                                        args.regex,
                                        args.not_contain,
                                        args.not_exact,
                                        args.not_regex)

    print(indexes)


if __name__ == "__main__":
    raise SystemExit(main())
