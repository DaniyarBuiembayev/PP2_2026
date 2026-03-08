import os

path = "workspace"

items = os.listdir(path)

for item in items:
    full_path = os.path.join(path, item)

    if os.path.isfile(full_path):
        print("File:", item)
    else:
        print("Folder:", item)