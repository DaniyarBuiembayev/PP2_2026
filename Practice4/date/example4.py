from datetime import datetime, date, timedelta
dt1 = datetime(2026, 2, 26, 12, 0, 0)   
dt2 = datetime(2026, 2, 25, 6, 30, 0)   
delta = dt1 - dt2
print(delta.total_seconds())