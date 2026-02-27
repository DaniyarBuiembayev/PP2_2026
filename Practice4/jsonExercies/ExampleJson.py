import json

with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("================================================================================")
print("DN                                                 Description          Speed   MTU  ")
print("-------------------------------------------------- -------------------- ------- -----")

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]
    
    print(f"{dn:50} {descr:20} {speed:7} {mtu:6}")