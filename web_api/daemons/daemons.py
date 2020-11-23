from biometric_poll import poll_predict
from music_recommender import recommend
import requests
import time

USER_ID = "skeletrox"
SINCE = "10m"

# URL to get user seed data
USER_SEED_URL = "https://127.0.0.1:8000/data/seeds/{}"

# URL to set recommendations
SET_RECS_URL = "https://127.0.0.1:8000/data/set_tracks/{}"

# URL to get heart rate data
GET_HR_URL = "https://127.0.0.1:8000/data/get_cutoffs/{}"

while True:
    results = poll_predict(USER_ID, SINCE)
    first_rate = results[0]
    last_rate = results[-1]
    r = requests.get(USER_SEED_URL.format(USER_ID), verify=False)
    seed_dict = r.json()
    r = requests.get(GET_HR_URL.format(USER_ID), verify=False)
    hr_dict = r.json()
    returnable = recommend(first_rate, last_rate, seed_dict["seeds"], hr_dict["cutoffs"])
    uris = [ret["uri"] for ret in returnable]
    r = requests.post(SET_RECS_URL.format(USER_ID), json={"heart_rate": last_rate, "track_list": uris}, verify=False)
    print(r.status_code)
    time.sleep(30)
