from utils_base.time.Time import Time
from utils_base.time.TimeFormat import TimeFormat


def get_date_id():
    return TimeFormat.DATE_ID.stringify(Time.now())
