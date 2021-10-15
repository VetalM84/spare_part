from django import template

from mileage.models import User

register = template.Library()


@register.simple_tag
def get_user_info(user_id):
    user = User.objects.get(id=user_id)
    return user

# @register.inclusion_tag('news/list_categories.html')
# def show_categories(arg1='Hello', arg2='world'):
#     categories = Category.objects.all()
#     return {"categories": categories, "arg1": arg1, "arg2": arg2}
