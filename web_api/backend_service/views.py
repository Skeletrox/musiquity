from django.shortcuts import render
from django.http import JsonResponse
from connectors.influxdb_connector import InfluxConnector
from django.views.decorators.csrf import csrf_exempt
from user_service.models import User
from .models import SeedList
import json
import redis

# Create your views here.

influx_conn_object = None

# initializes the influx connector object if it hasn't been done already
def initialize_influx_conn_object():
    global influx_conn_object
    influx_conn_object = InfluxConnector()
    influx_conn_object.auth(host="localhost", port=7086, database="user_metrics")
    influx_conn_object.create(database="user_metrics")
    influx_conn_object.additional(database_switch="user_metrics")


# telemetry upload middleware
@csrf_exempt
def upload_telemetry(request):
    global influx_conn_object
    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': 'Expected POST'})

    json_body = json.loads(request.body.decode("utf-8"))
    user_id = json_body['user_id']
    heart_rate = json_body['heart_rate']
    movement = json_body['movement']
    timestamp = json_body['timestamp']

    if influx_conn_object is None:
        initialize_influx_conn_object()

    writable_json = [
        {
            "measurement": "biometrics",
            "tags": {
                "user_id": user_id
            },
            "time": timestamp,
            "fields": {
                "heart_rate": heart_rate,
                "movement": movement
            }
        }
    ]
    influx_conn_object.create(points=writable_json, time_precision="s")
    return JsonResponse({'success': True, 'msg': 'Points Written'})


# telemetry download middleware
def read_points(request,user,since):
    global influx_conn_object
    if influx_conn_object is None:
        initialize_influx_conn_object()

    prepared_query = "SELECT timestamp, heart_rate, movement FROM biometrics WHERE user_id = '{}' and time > now() - {}".format(user, since)
    points = influx_conn_object.read(query=prepared_query)
    returnable = [p for p in points["biometrics"]]
    return JsonResponse({'success': True, 'points': returnable})


# get seed list
def get_seed_list(request,user):
    my_user = User.objects.get(user_id=user)
    seed_lists = SeedList.objects.filter(user=my_user)
    returnable = {}
    for s in seed_lists:
        returnable[s.mode] = s.seed_list

    return JsonResponse({'success': True, 'user_id': user, 'seeds': returnable})


# get current user data from redis
def get_user_from_redis(request,user):
    pass