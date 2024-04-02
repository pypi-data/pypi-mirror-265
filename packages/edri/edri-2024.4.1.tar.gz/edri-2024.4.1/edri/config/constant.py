from enum import Enum, IntEnum, unique

SWITCH_NEW_DEMANDS = (18446744073709551615).to_bytes(8, "big", signed=False)
SWITCH_LAST_MESSAGES = (18446744073709551614).to_bytes(8, "big", signed=False)

SCHEDULER_TIMEOUT_MAX = 2147483  # INT_MAX bez posledních tří čísel
STREAM_CLOSE_MARK = "#&@"


@unique
class ApiType(IntEnum):
    WS = 0
    REST = 1
