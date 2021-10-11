from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('car/<int:car_id>/', get_car_spare_parts, name='car_spare_parts'),
    path('spare_part/<int:car_id>/<int:spare_part_id>/', get_spare_parts_mileages, name='spare_parts_mileages'),
]
