from django.urls import path
from . import views

urlpatterns = [
    path('new', views.upload_telemetry, name='put'),
    path('read/<user>/<since>', views.read_points, name='get')
]