import sys
from datetime import datetime, timezone, timedelta
import calendar

def parse(line):
    date_part, tz_part = line.strip().split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    tz = timezone(offset)
    return dt.replace(tzinfo=tz), tz

birth_dt, birth_tz = parse(sys.stdin.readline())
current_dt, current_tz = parse(sys.stdin.readline())

current_utc = current_dt.astimezone(timezone.utc)

def birthday_in_year(year):
    month = birth_dt.month
    day = birth_dt.day
    if month == 2 and day == 29 and not calendar.isleap(year):
        day = 28
    b = datetime(year, month, day, tzinfo=birth_tz)
    return b.astimezone(timezone.utc)

year = current_dt.year
candidate = birthday_in_year(year)

if candidate < current_utc:
    candidate = birthday_in_year(year + 1)

diff = candidate - current_utc
print(diff.days)