""" aiocomfoconnect library """

DEFAULT_UUID = "00000000000000000000000000000001"
DEFAULT_PIN = 0
DEFAULT_NAME = "aiocomfoconnect"

from .bridge import Bridge  # noqa: E402
from .comfoconnect import ComfoConnect  # noqa: E402
from .discovery import discover_bridges  # noqa: E402
