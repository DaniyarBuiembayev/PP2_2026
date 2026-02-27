import json
import sys
import re

data = json.loads(sys.stdin.readline())
q = int(sys.stdin.readline())

pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)|\[(\d+)\]')

for _ in range(q):
    query = sys.stdin.readline().strip()
    current = data
    ok = True

    for match in pattern.finditer(query):
        key, index = match.groups()
        if key is not None:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                ok = False
                break
        else:
            idx = int(index)
            if isinstance(current, list) and 0 <= idx < len(current):
                current = current[idx]
            else:
                ok = False
                break

    if ok:
        print(json.dumps(current, separators=(',', ':')))
    else:
        print("NOT_FOUND")