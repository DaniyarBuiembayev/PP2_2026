import os
import shutil

os.makedirs("workspace/project/data/raw", exist_ok=True)

source = "../file_handling/sample.txt"
destination = "workspace/project/sample_copy.txt"

shutil.copy(source, destination)

print("File copied!")

shutil.move(
    "workspace/project/sample_copy.txt",
    "workspace/project/data/raw/sample_moved.txt"
)

print("File moved!")