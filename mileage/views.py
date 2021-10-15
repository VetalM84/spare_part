from django.shortcuts import render
from django.db.models import Avg, Max, Min

from .models import Car, Mileage


def index(request):
    """ получаем список всех добавленных авто без учета записей о пробеге запчастей """
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'title': 'Список автомобилей',
    }
    return render(request, template_name='mileage/index.html', context=context)


def get_car_spare_parts(request, car_id):
    """ получаем список запчастей для конкретной марки и модели авто """
    # TODO сделать DISTINCT
    spare_parts = Mileage.objects.filter(car_id=car_id)
    # car = Car.objects.get(id=car_id)
    context = {
        'spare_parts': spare_parts,
        'title': 'Список запчастей для',
        # 'model_name': car.model_name,
        # 'brand': car.brand,
        # 'car_age': car.age,

    }
    return render(request, 'mileage/car.html', context)


def get_spare_parts_mileages(request, car_id, spare_part_id):
    """ получаем список всех записей о пробеге для конкретной запчасти на конкретной марке и модели авто """
    spare_parts = Mileage.objects.filter(car_id=car_id, spare_part_id=spare_part_id).order_by('-mileage')
    max_mileage = spare_parts.aggregate(Max('mileage'))
    min_mileage = spare_parts.aggregate(Min('mileage'))
    avg_mileage = spare_parts.aggregate(Avg('mileage'))
    records_count = spare_parts.count()

    # car = Car.objects.get(id=car_id)
    # список похожих запчастей по имени запчасти исключая текущую
    # current_spare_part_name = SparePart.objects.get(id=spare_part_id).name
    # similar_spare_parts = SparePart.objects.filter(name__contains=current_spare_part_name)
    similar_spare_parts = Mileage.objects.filter(car_id=car_id, spare_part__name__contains=spare_parts.first().
                                                 spare_part.name).exclude(spare_part_id=spare_part_id)

    context = {
        'spare_parts': spare_parts,
        'similar_spare_parts': similar_spare_parts,
        'title': 'Список пробегов запчасти для',
        # 'model_name': car.model_name,
        # 'model_variant': car.model_variant,
        # 'brand': car.brand,
        # 'car_age': car.age,
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'records_count': records_count,
    }
    return render(request, 'mileage/spare_part.html', context)


def get_user_profile(request, user_id):
    user_reports = Mileage.objects.filter(owner_id=user_id)
    context = {
        'title': 'Мой профиль',
        'user_reports': user_reports
    }
    return render(request, 'mileage/user_profile.html', context)

