import os

search_path = "workspace"

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith(".txt"):
            print("Found:", os.path.join(root, file))