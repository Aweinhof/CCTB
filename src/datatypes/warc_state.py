from enum import Enum


class WarcState(Enum):
    NONE = 0,
    START_META = 1,
    REQUEST_WARC_META = 2,
    REQUEST_META = 3,
    RESPONSE_WARC_META = 4,
    RESPONSE_META = 5,
    RESPONSE = 6,
    POST_WARC_META = 7,
    POST_META = 8
