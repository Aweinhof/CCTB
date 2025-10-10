from src.datatypes.warc_state import WarcState
from src.logger import error


class StructureTester:
    current_line = ""
    base_line = ""

    def convert_state(self, state):
        match state:
            case WarcState.NONE:
                return "none"
            case WarcState.START_META:
                return "start_meta"
            case WarcState.REQUEST_WARC_META:
                return "request_warc_meta"
            case WarcState.REQUEST_META:
                return "request_meta"
            case WarcState.RESPONSE_WARC_META:
                return "response_warc_meta"
            case WarcState.RESPONSE_META:
                return "response_meta"
            case WarcState.RESPONSE:
                return "response"
            case WarcState.POST_WARC_META:
                return "post_warc_meta"
            case WarcState.POST_META:
                return "post_meta"
            case _:
                return "Not Found"

    def add_state(self, state, file_line):
        state_str = self.convert_state(state)

        if state_str not in self.current_line.split('\n') or \
           state is WarcState.NONE:
            self.current_line += state_str + "\n"

        else:
            if not self.base_line:
                self.base_line = self.current_line
                self.current_line = state_str + "\n"

            elif self.current_line != self.base_line:
                error("Different struct found :\n\n\nBase struct :\n\n"
                      + self.base_line + "\n\n\nCurrent struct :\n\n" + self.current_line
                      + "\n\nLast known line in chunk file : " + str(file_line))
                exit(1)
            else:
                self.current_line = state_str + "\n"

    def print(self):
        if self.base_line:
            print("Structure order verified : \n" + self.base_line)
