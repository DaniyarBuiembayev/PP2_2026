import json
import sys

def deep_diff(a, b, path=""):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        keys = sorted(set(a.keys()) | set(b.keys()))
        for key in keys:
            new_path = f"{path}.{key}" if path else key
            if key not in a:
                diffs.append((new_path, "<missing>", json.dumps(b[key], separators=(',', ':'))))
            elif key not in b:
                diffs.append((new_path, json.dumps(a[key], separators=(',', ':')), "<missing>"))
            else:
                diffs.extend(deep_diff(a[key], b[key], new_path))
    else:
        if a != b:
            diffs.append((
                path,
                json.dumps(a, separators=(',', ':')),
                json.dumps(b, separators=(',', ':'))
            ))
    return diffs

obj1 = json.loads(sys.stdin.readline())
obj2 = json.loads(sys.stdin.readline())

differences = deep_diff(obj1, obj2)

if not differences:
    print("No differences")
else:
    for path, old, new in sorted(differences):
        print(f"{path} : {old} -> {new}")