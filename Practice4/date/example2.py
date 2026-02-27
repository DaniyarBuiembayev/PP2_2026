from datetime import date, timedelta
x = date.today()
yesterday = x - timedelta(days = 1)
tomorrow = x + timedelta(days = 1)
print(yesterday)
print(x)
print(tomorrow)