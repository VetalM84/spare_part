from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('car_models/<int:car_id>/', get_car_models, name='car_models_all'),
    path('model/<int:model_id>/', get_model_info, name='model_info'),
    path('category/<int:category_id>/', get_spare_parts_category, name='spare_parts_category'),
    path('categories/', get_all_spare_parts_categories, name='get_spare_parts_categories'),
    path('new_spare_part/', add_new_spare_part, name='new_spare_part'),
    path('add_review/', add_review, name='add_review_page'),
    path('search/', search, name='search_page'),
    path('user/', get_user_profile, name='user_profile_page'),
    path('user_public/<int:user_id>/', get_public_user_profile, name='user_public_profile_page'),
    path('spare_part/<int:spare_part_id>/', get_spare_part, name='get_spare_part'),
    path('model_spare_part/<int:model_id>/<int:spare_part_id>/', get_model_spare_parts_reviews,
         name='model_spare_parts_reviews'),
    path('get_models/<int:brand_id>/', get_chained_car_models, name='ajax_get_chained_car_models'),
    path('spare_part_autocomplete/', SparePartAutocomplete.as_view(), name='spare_part_autocomplete'),
    path('like/', like, name='like'),
    path('add_comment/', add_comment, name='add_comment'),
]

