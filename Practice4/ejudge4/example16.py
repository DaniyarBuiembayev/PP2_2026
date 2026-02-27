import sys
from datetime import datetime, timezone, timedelta

def parse(line):
    parts = line.strip().split()
    date_part = parts[0]
    time_part = parts[1]
    tz_part = parts[2]
    dt = datetime.strptime(date_part + " " + time_part, "%Y-%m-%d %H:%M:%S")
    sign = 1 if tz_part[3] == '+' else -1
    hours = int(tz_part[4:6])
    minutes = int(tz_part[7:9])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    return dt.replace(tzinfo=timezone(offset)).astimezone(timezone.utc)

start = parse(sys.stdin.readline())
end = parse(sys.stdin.readline())

diff = end - start
print(int(diff.total_seconds()))