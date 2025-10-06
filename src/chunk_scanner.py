from src.datatypes.warc_state import WarcState
from src.structure_tester import StructureTester

class ChunkScanner:
    state = WarcState.START_META
    struct_tester = StructureTester()
    iteration = 0

    def __init__(self):
        pass

    def state_change_end_response(self, line):
        if self.state is WarcState.RESPONSE and line == b"WARC/1.0":
            self.state = WarcState.NONE
            return True
        return False

    def state_change_line_match(self, line):
        line = line.strip()

        match line:
            case b"WARC-Type: request":
                self.state = WarcState.REQUEST_WARC_META

            case b"WARC-Type: response":
                self.state = WarcState.RESPONSE_WARC_META

            case b"WARC-Type: metadata":
                self.state = WarcState.POST_WARC_META

            case _:
                return False

        return True

    def state_change_empty_line(self, line):
        # if empty line
        if not line.strip():

            match self.state:
                case WarcState.REQUEST_WARC_META:
                    self.state = WarcState.REQUEST_META

                case WarcState.RESPONSE_WARC_META:
                    self.state = WarcState.RESPONSE_META

                case WarcState.POST_WARC_META:
                    self.state = WarcState.POST_META

                case WarcState.REQUEST_META:
                    self.state = WarcState.NONE

                case WarcState.RESPONSE_META:
                    self.state = WarcState.RESPONSE

                case WarcState.POST_META:
                    self.state = WarcState.NONE

                case _:
                    return False

            return True
        return False

    def state_change(self, line):
        if self.state_change_line_match(line) or \
           self.state_change_empty_line(line) or \
           self.state_change_end_response(line):
            # self.struct_tester.add_state(self.state, self.iteration)    # to comment in production
            return True
        return False

    def treat_chunk_line(self, line):
        match self.state:
            case WarcState.START_META | WarcState.NONE:
                return True

            case WarcState.REQUEST_WARC_META:
                return True

            case WarcState.REQUEST_META:
                return True

            case WarcState.RESPONSE_WARC_META:
                return True

            case WarcState.RESPONSE_META:
                return True

            case WarcState.RESPONSE:
                return True

            case WarcState.POST_WARC_META:
                return True

            case WarcState.POST_META:
                return True

        return False

    def scan(self, path):
        with open(path, 'rb') as f:

            while line := f.readline():
                self.iteration += 1
                if self.state_change(line):
                    continue

                if self.treat_chunk_line(line):
                    continue

        self.struct_tester.print()

    def fast_scan(self, path, regex):
        # grep ;)
        pass
