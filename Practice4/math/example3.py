import math
sides = float(input("Input number of sides: "))
length_of_side = float(input("Input the length of a side: "))
Area = round((sides*pow(length_of_side, 2))/4*math.tan(math.pi/sides))
print(f"The area of the polygon is: {Area}")