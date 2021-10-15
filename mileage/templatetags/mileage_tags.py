from django import template

from mileage.models import User, Car

register = template.Library()


@register.simple_tag
def get_user_info(user_id):
    user = User.objects.get(id=user_id)
    return user


@register.simple_tag
def get_car_info(car_id):
    car = Car.objects.get(id=car_id)
    return car

# @register.inclusion_tag('news/list_categories.html')
# def show_categories(arg1='Hello', arg2='world'):
#     categories = Category.objects.all()
#     return {"categories": categories, "arg1": arg1, "arg2": arg2}
