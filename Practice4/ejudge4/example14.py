import sys
from datetime import datetime, timezone, timedelta

def parse_line(line):
    date_part, tz_part = line.strip().split()
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    return dt.replace(tzinfo=timezone(offset)).astimezone(timezone.utc)

dt1 = parse_line(sys.stdin.readline())
dt2 = parse_line(sys.stdin.readline())

diff = abs(dt1 - dt2)
print(diff.days)