from utils_base.time.TimeUnit import TimeUnit

SECOND = TimeUnit(1)
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7
FORTNIGHT = WEEK * 7

AVG_YEAR = DAY * 365.25
AVG_QTR = AVG_YEAR / 4
AVG_MONTH = AVG_YEAR / 12


class DAYS_IN:  # noqa
    AVG_MONTH = TimeUnit.AVG_MONTH / TimeUnit.DAY
    AVG_QTR = TimeUnit.AVG_QTR / TimeUnit.DAY
    AVG_YEAR = TimeUnit.AVG_YEAR / TimeUnit.DAY
