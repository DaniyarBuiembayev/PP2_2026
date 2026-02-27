import importlib

n = int(input())
for _ in range(n):
    line = input().strip()
    module_path, attribute_name = line.split()
    
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue
    
    if not hasattr(module, attribute_name):
        print("ATTRIBUTE_NOT_FOUND")
        continue
    
    attr = getattr(module, attribute_name)
    if callable(attr):
        print("CALLABLE")
    else:
        print("VALUE")