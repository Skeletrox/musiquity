import json
from sys import version_info
import requests
import time

POST_URL = "https://127.0.0.1:8000/data/new"

with open('./points.txt') as points:
    values = json.loads(points.read())

numvals = len(values)
for i, v in enumerate(values):
    delay = 0 if i == numvals - 1 else values[i+1]["timestamp"] - v["timestamp"]
    v["timestamp"] = int(time.time())
    r = requests.post(POST_URL, json=v, verify=False)
    print(r.status_code)
    time.sleep(delay)