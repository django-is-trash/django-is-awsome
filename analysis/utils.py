from datetime import date, timedelta
import calendar


# DAILY (오늘)
def get_daily_range():
    today = date.today()
    return today, today


# LAST DAY (어제)
def get_last_day_range():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday, yesterday


# WEEKLY (이번 주)
def get_week_range():
    today = date.today()
    monday = today - timedelta(days=today.weekday())   # weekday(): Monday=0 ~ Sunday=6
    sunday = monday + timedelta(days=6)
    return monday, sunday


# LAST WEEK (지난 주)
def get_last_week_range():
    today = date.today()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    return last_monday, last_sunday


# MONTHLY (이번 달)
def get_month_range():
    today = date.today()
    first_day = date(today.year, today.month, 1)
    last_day = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    return first_day, last_day


# LAST MONTH (지난 달)
def get_last_month_range():
    today = date.today()
    first_day_this_month = date(today.year, today.month, 1)

    last_day_last_month = first_day_this_month - timedelta(days=1)
    first_day_last_month = date(last_day_last_month.year, last_day_last_month.month, 1)

    return first_day_last_month, last_day_last_month


# YEARLY (올해)
def get_year_range():
    today = date.today()
    first_day = date(today.year, 1, 1)
    last_day = date(today.year, 12, 31)
    return first_day, last_day


# LAST YEAR (작년)
def get_last_year_range():
    today = date.today()
    last_year = today.year - 1
    first_day = date(last_year, 1, 1)
    last_day = date(last_year, 12, 31)
    return first_day, last_day
