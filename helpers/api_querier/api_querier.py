from sys import argv
import requests
import time
from copy import deepcopy
import json

token_file_path = argv[1]

REQUEST_SKELETON = "https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm/datasets/{}-{}"
POST_URL = "https://127.0.0.1:8000/data/new"

with open(token_file_path) as tkf:
    token = tkf.read()

headers = {
    "Content-Type": "application/json;encoding=utf-8",
    "Authorization": "Bearer {}".format(token)
}


MEASUREMENT_TEMPLATE = {
        "user_id" : "skeletrox",
        "heart_rate": 80,
        "movement": 1,
        "timestamp": None
    }

def poll():
    curr_ts_s = int(time.time())
    curr_ts = int(curr_ts_s*1e9)
    old_ts = int((curr_ts_s - 3600)*1e9)
    req_url = REQUEST_SKELETON.format(old_ts, curr_ts)
    r = requests.get(req_url, headers=headers)

    response = r.json()

    writable = []

    print(response)
    for p in response["point"]:
        try:
            timestamp = int(((int(p["startTimeNanos"]) + int(p["endTimeNanos"])) // 2) // 1e9)
            hr = p["value"][0]["fpVal"]
            current_body = deepcopy(MEASUREMENT_TEMPLATE)
            current_body["heart_rate"] = hr
            current_body["timestamp"] = timestamp
            writable.append(current_body)
        except Exception as e:
            print(e)

    return writable


def main():
    while(True):
        result = poll()
        if result:
            with open('points.txt', 'w') as points:
                points.write(json.dumps(result))
            # for z in result:
            #    r = requests.post(POST_URL, json=z, verify=False)
            #    print(r.status_code)
        else:
            print("no data")

        time.sleep(30)


if __name__ == "__main__":
    main()