from datetime import datetime
from typing import Union, Tuple


def _loop_fetch(src, *args):
    fetch_key = args[0]
    fetch_result = src.get(fetch_key)
    return fetch_result if len(args) == 1 else _loop_fetch(fetch_result, args[1:])


def _covert_type(src, covert_type: Union[type] = None, covert_format: Union[str] = None):
    if isinstance(src, covert_type):
        return src
    if isinstance(src, str) and covert_type == datetime:
        return datetime.strptime(src, covert_format)
    if isinstance(src, str) and covert_type == int:
        return int(src, covert_format or 10)
    if isinstance(src, int) and covert_type == str:
        return '0x{:02X}'.format(src) if covert_format == '16' else str(src)
    return covert_type(src)


def fetch(src: Union[dict],
          *args: Tuple[str],
          default=None,
          covert_type: Union[type] = None,
          covert_format: Union[str] = None):
    if not src or not args:
        return None
    try:
        fetch_result = _loop_fetch(src, args)
        covert_result = _covert_type(fetch_result, covert_type, covert_format)
        return covert_result
    except Exception as e:
        if default is not None:
            return default
        raise e
