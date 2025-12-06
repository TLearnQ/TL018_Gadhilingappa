# json and yaml


import json, yaml

file_path = r"C:\Users\ADMIN\OneDrive\Desktop\telcom\assessment\demo.json"

json ="""
{"config":{"site": "Banglore", "devices": 12}}

"""

def key(d):
    if isinstance(d, dict):
        return {k.lower(): key(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [key(i) for i in d]
    
    
    
def config(file, output):
    if file.endswith(".json"):
        data = json.load(open(file))
    else:
        data = yaml.safe_load(open(file))
    
    clean = key(data)
    with open(r"demo_output.json","w") as f:
        json.dump(clean, f, indent=4)
        print("save the output :{demo_output.json}")
        
    return clean






















