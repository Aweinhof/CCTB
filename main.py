from src.parser import build_parser
import sys
from src.cctb import CCTB
from src.chunks_parser import ChunksParser
from src.typo_fuzzer import TypoFuzzer
from src.routine import routine_check


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


def scan_chunk(args):
    cctb = CCTB()
    cctb.scan_chunk(args.chunk_path)


def phishing(args):
    cctb = CCTB()
    cctb.phishing(args.auto, args.hostname)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = build_parser().parse_args(argv)

    routine_check()

    match args.command:
        case "find":
            find(args)

        case "chunks":
            chunks(args)

        case "scan_chunk":
            scan_chunk(args)

        case "phishing":
            phishing(args)


if __name__ == "__main__":
    raise SystemExit(main())
