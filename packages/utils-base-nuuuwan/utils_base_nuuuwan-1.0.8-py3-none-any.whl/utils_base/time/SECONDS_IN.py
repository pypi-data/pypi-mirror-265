from utils_base.time.TimeUnit import TimeUnit


class SECONDS_IN:  # noqa
    MINUTE = TimeUnit.MINUTE / TimeUnit.SECOND
    HOUR = TimeUnit.HOUR / TimeUnit.SECOND
    DAY = TimeUnit.DAY / TimeUnit.SECOND
    WEEK = TimeUnit.WEEK / TimeUnit.SECOND
    FORTNIGHT = TimeUnit.FORTNIGHT / TimeUnit.SECOND

    AVG_MONTH = TimeUnit.AVG_MONTH / TimeUnit.SECOND
    AVG_QTR = TimeUnit.AVG_QTR / TimeUnit.SECOND
    AVG_YEAR = TimeUnit.AVG_YEAR / TimeUnit.SECOND
