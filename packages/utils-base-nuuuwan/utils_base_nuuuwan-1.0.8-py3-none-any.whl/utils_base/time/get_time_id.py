from utils_base.time.Time import Time
from utils_base.time.TimeFormat import TimeFormat


def get_time_id():
    return TimeFormat.TIME_ID.stringify(Time.now())
