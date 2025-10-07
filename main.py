from src.parser import build_parser
import sys
from src.cctb import CCTB
from src.chunks_parser import ChunksParser
from src.typo_fuzzer import TypoFuzzer


def find(args):
    if args.typo_fuzz:
        fuzzer = TypoFuzzer(args.host)
        fuzzer.fuzz()

    else:
        cctb = CCTB()
        indexes = cctb.get_indexes_filtered(args.host,
                                            args.contain,
                                            args.exact,
                                            args.regex,
                                            args.not_contain,
                                            args.not_exact,
                                            args.not_regex)
        print(indexes)


def chunks(args):
    p = ChunksParser(args.dataset_id)
    p.print()


def find_page():
    cctb = CCTB()
    cctb.scan_chunk('/home/csirc/Workspace/CCTB/junk/warc_type/CC-MAIN-20250905112101-20250905142101-00000.warc')


def dev():
    cctb = CCTB()
    cctb.dev()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)

    match args.command:
        case "find":
            find(args)

        case "chunks":
            chunks(args)

        case "find_page":
            find_page()

        case "dev":
            dev()


if __name__ == "__main__":
    raise SystemExit(main())
