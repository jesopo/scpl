import string
from typing import Dict

RANGES: Dict[int, str] = {}
RANGE_CHARS: Dict[int, int] = {}
def _addrange(range: int, chars: str):
    RANGES[range] = chars
    for char in chars:
        RANGE_CHARS[ord(char)] = range

_addrange(0, string.ascii_lowercase)
_addrange(1, string.ascii_uppercase)
_addrange(2, string.digits)

def get_range(start: int, end: int) -> str:
    range = RANGES[RANGE_CHARS[start]]
    r_start = range.find(chr(start))
    return range[r_start:range.find(chr(end))+1]
