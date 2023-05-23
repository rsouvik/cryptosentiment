import datetime
from datetime import time

from pytz import timezone

"""def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = datetime.time
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset """


def datetime_from_utc_to_local(utc_datetime):
    # fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    fmt = "%Y-%m-%d %H:%M:%S"
    now_pacific = utc_datetime.astimezone(timezone('US/Pacific'))
    return now_pacific.strftime(fmt)
