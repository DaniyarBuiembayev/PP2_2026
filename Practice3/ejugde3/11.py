class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self, other):
        return Pair(self.a + other.a, self.b + other.b)


x1, y1, x2, y2 = map(int, input().split())

p1 = Pair(x1, y1)
p2 = Pair(x2, y2)

result = p1.add(p2)

print(f"Result: {result.a} {result.b}")