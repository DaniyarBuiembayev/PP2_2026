import sys
import math

r = float(sys.stdin.readline())
x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

def dist(x, y):
    return math.hypot(x, y)

d = math.hypot(x2 - x1, y2 - y1)

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r
disc = b*b - 4*a*c

intersects = False
if disc > 0:
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)
    if (0 <= t1 <= 1) or (0 <= t2 <= 1):
        intersects = True

if not intersects:
    print(f"{d:.10f}")
else:
    d1 = dist(x1, y1)
    d2 = dist(x2, y2)
    theta = math.acos((x1*x2 + y1*y2) / (d1*d2))
    alpha1 = math.acos(r / d1)
    alpha2 = math.acos(r / d2)
    arc = theta - alpha1 - alpha2
    length = math.sqrt(d1*d1 - r*r) + math.sqrt(d2*d2 - r*r) + r * arc
    print(f"{length:.10f}")