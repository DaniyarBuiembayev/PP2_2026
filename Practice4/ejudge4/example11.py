import json
import sys

def apply_patch(source, patch):
    for key in patch:
        if patch[key] is None:
            if key in source:
                del source[key]
        elif key in source and isinstance(source[key], dict) and isinstance(patch[key], dict):
            apply_patch(source[key], patch[key])
        else:
            source[key] = patch[key]
    return source

source = json.loads(sys.stdin.readline())
patch = json.loads(sys.stdin.readline())

result = apply_patch(source, patch)

print(json.dumps(result, separators=(',', ':'), sort_keys=True))