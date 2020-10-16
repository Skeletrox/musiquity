# writes data to influxdb in 1s intervals

from connectors.influxdb_connector import InfluxConnector
from copy import deepcopy
from datetime import datetime
import math
from scipy.stats import norm
import time

# change in heartbeat, just some dummy data
UPWARDS_HEART_CHANGE = 600 # your heart rate reaches the peak in 10m
DOWNWARDS_HEART_CHANGE = 900 # your heart rate comes back to normal in 15m
HEART_CHANGE_POST_WORKOUT = 180 # your heart rate reaches stressed levels in 3m

# define constants in a dict
TARGET_HEART_RATE_DICT = {
    "RELAX": 75,
    "RUN": 160,
    "WEIGHTS": 105,
    "POST_WORKOUT": 100
}

MEASUREMENT_TEMPLATE = {
        "measurement": "biometrics",
        "tags": {
            "user_id": 1,
        },
        "time": None,
        "fields": {
            "heart_rate": 85,
            "movement": 0
        }
    }

def generate_json_body(activity, time_delta, init_data, freq_logging=3):
    """
        Generates a JSON body for the appropriate activity
        
        @param activity: The activity that is being performed
        @param time_delta: The amount of time the activty is performed
        @param init_data: The initial date (heart rate, timestamp)
        @param freq_logging: The frequency of logging
    """
    init_heart_rate = init_data["heart_rate"]
    init_timestamp = init_data["timestamp"]
    target_heart_rate = TARGET_HEART_RATE_DICT[activity]
    delta_heart_rate = (target_heart_rate - init_heart_rate) / (HEART_CHANGE_POST_WORKOUT if activity == "POST_WORKOUT" else UPWARDS_HEART_CHANGE if target_heart_rate > init_heart_rate else DOWNWARDS_HEART_CHANGE)
    current_heart_rate = init_heart_rate

    # build a normal distribution curve for your heart rate
    mean = abs(target_heart_rate - init_heart_rate) / 2
    # Assume that the target is 2 stds from the mean
    distrib = norm(loc=mean, scale=abs(target_heart_rate - mean) / 2)

    returnable_list = []
    for i in range(0,time_delta*60,freq_logging):
        # time_delta is expressed in minutes, but we log data each freq_logging seconds
        if math.log(current_heart_rate/target_heart_rate)*delta_heart_rate < 0:
            # Let's break down the log function
            # We need current heart rate to update when delta heart rate is positive and current rate < target rate
            # And when delta heart rate is negative and current rate > target rate
            # So the log of (CR/HR) > 0 if CR > HR and < 0 if CR < HR. Multiply that with delta and take the sign
            current_heart_rate += delta_heart_rate*(1+distrib.pdf(current_heart_rate))
        current_body = deepcopy(MEASUREMENT_TEMPLATE)
        current_body["fields"]["heart_rate"] = current_heart_rate
        current_body["fields"]["movement"] = 0 if activity in ["RELAX", "POST_WORKOUT"] else 1
        current_body["time"] = int(init_timestamp + i)
        returnable_list.append(current_body)


    init_data["heart_rate"] = current_heart_rate
    init_data["timestamp"] = init_timestamp + time_delta*60
    return init_data, returnable_list
    
    
connector = InfluxConnector()
connector.auth(host="localhost", port=7086, database="user_metrics")
connector.create(database="user_metrics")
connector.additional(database_switch="user_metrics")
spoof_data = []
with open("spoof_schedule.txt", "r") as spoof:
    spoof_data = spoof.read().split("\n")
metadata = {
    "heart_rate": 70,
    "timestamp": time.time()
}
for datum in spoof_data:
    [activity, curr_time] = datum.strip().split(" ")
    metadata, appendable = generate_json_body(activity, int(curr_time), metadata)
    for a in appendable:
        connector.create(points=[a], time_precison="s")
        time.sleep(3)
        print("Point written.")