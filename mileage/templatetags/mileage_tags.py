from django import template
from django.shortcuts import get_object_or_404

from mileage.models import User, Car

register = template.Library()


@register.simple_tag
def get_user_info(user_id):
    # user = User.objects.get(id=user_id)
    user = get_object_or_404(User, pk=user_id)
    return user


@register.simple_tag
def get_car_info(car_id):
    # car = Car.objects.get(id=car_id)
    car = get_object_or_404(Car, pk=car_id)
    return car
