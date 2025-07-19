import json

def work_json():
    data = json.loads('{"x":1,"y":2}')
    print("Loaded:", data)
    out = json.dumps(data)
    print("Dumped:", out)

if __name__ == "__main__":
    work_json()
