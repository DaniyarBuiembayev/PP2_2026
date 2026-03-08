with open("sample.txt", "a") as file:
    file.write("\nMilk - 2.30\n")
    file.write("Bread - 1.10\n")
    file.write("Eggs - 3.20\n")

print("New items added.")


with open("sample.txt", "r") as file:
    print(file.read())