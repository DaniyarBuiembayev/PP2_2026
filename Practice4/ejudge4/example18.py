import sys

x1, y1 = map(float, sys.stdin.readline().split())
x2, y2 = map(float, sys.stdin.readline().split())

x_ref = (x1 * y2 + x2 * y1) / (y1 + y2)
y_ref = 0.0

print(f"{x_ref:.10f} {y_ref:.10f}")