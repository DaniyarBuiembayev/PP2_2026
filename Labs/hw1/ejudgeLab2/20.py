n = int(input())

doc = {}

for _ in range(n):
    command = input().split()

    if command[0] == "set":
        key = command[1]
        value = command[2]
        doc[key] = value

    elif command[0] == "get":
        key = command[1]
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")
