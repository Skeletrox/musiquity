from django.urls import path
from . import views

urlpatterns = [
    path('new', views.upload_telemetry, name='put'),
    path('read/<user>/<since>', views.read_points, name='get'),
    path('seeds/<user>', views.get_seed_list, name='get_seed_list'),
    path('set_tracks/<user>', views.set_user_in_redis, name='put_redis'),
    path('get_tracks/<user>', views.get_user_from_redis, name='get_redis'),
    path('update_cutoffs/<user>', views.set_heart_rate, name='update_cutoffs'),
    path('get_cutoffs/<user>', views.get_heart_rate, name='get_cutoffs'),
]