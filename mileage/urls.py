from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('car_models/<int:car_id>/', get_car_models, name='car_models_all'),
    path('model/<int:model_id>/', get_model_info, name='model_info'),
    path('category/<int:category_id>/', get_spare_parts_category, name='spare_parts_category'),
    # path('car/<int:car_id>/', get_car_spare_parts, name='car_spare_parts'),
    path('user/<int:user_id>/', get_user_profile, name='user_profile_page'),
    path('spare-part/<int:car_id>/<int:spare_part_id>/', get_spare_parts_mileages, name='spare_parts_mileages'),
    path('add-mileage/', add_mileage, name='add_mileage_page'),
    path('mileage/ajax/load-models/', load_models, name='ajax_load-models'),
]
