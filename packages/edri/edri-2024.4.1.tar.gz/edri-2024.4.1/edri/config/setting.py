from os import getenv
from typing import Optional

HEALTH_CHECK_TIMEOUT = getenv("EDRI_HEALTH_CHECK_TIMEOUT") or 10
TOKEN_LENGTH = getenv("EDRI_TOKEN_LENGTH") or 64
REST_RESPONSE_TIMEOUT = getenv("EDRI_REST_RESPONSE_TIMEOUT") or 60

SWITCH_KEY_LENGTH = getenv("EDRI_SWITCH_KEY_LENGTH ") or 8
SWITCH_HOST = getenv("EDRI_SWITCH_HOST")
SWITCH_PORT = getenv("EDRI_SWITCH_POST")

UPLOAD_FILES_PREFIX = getenv("EDRI_UPLOAD_FILES_PREFIX") or "edri_"
UPLOAD_FILES_KEEP_DAYS = getenv("EDRI_FILES_KEEP_DAYS") or 0
UPLOAD_FILES_PATH = getenv("EDRI_FILES_PATH") or "/tmp/edri"

CACHE_TIMEOUT = getenv("EDRI_CACHE_TIMEOUT") or 30
CACHE_INFO_MESSAGE = getenv("EDRI_CACHE_INFO_MESSAGE") or 60

HOST = getenv("EDRI_HOST") or "localhost"
ws_port_temp = getenv("EDRI_WS_PORT")
WS_PORT: Optional[int] = None
if ws_port_temp:
    WS_PORT = int(ws_port_temp)
else:
    WS_PORT = 8877

rest_port_temp = getenv("EDRI_REST_PORT")
REST_PORT: Optional[int] = None
if rest_port_temp:
    REST_PORT = int(rest_port_temp)
else:
    REST_PORT = 8878
