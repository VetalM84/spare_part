from django.shortcuts import render

from .models import Car, SparePart, Mileage


def index(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
        'title': 'Список автомобилей',
    }
    return render(request, template_name='mileage/index.html', context=context)


def get_car_spare_parts(request, car_id):
    # TODO сделать DISTINCT
    spare_parts = Mileage.objects.filter(car_id=car_id)
    car = Car.objects.get(id=car_id)
    context = {
        'spare_parts': spare_parts,
        'title': 'Список запчастей для',
        'model_name': car.model_name,
        'brand': car.brand,
        'car_age': car.age,

    }
    return render(request, 'mileage/car.html', context)


def get_spare_parts_mileages(request, car_id, spare_part_id):
    spare_parts = Mileage.objects.filter(car_id=car_id, spare_part_id=spare_part_id)
    # reports = spare_parts.filter(spare_part_id)
    # car = Car.objects.get(id=spare_part_id)
    context = {
        'spare_parts': spare_parts,
        # 'reports': reports,
        'title': 'Список пробегов запчасти для',
        # 'model_name': car.model_name,
        # 'brand': car.brand,
        # 'car_age': car.age,

    }
    return render(request, 'mileage/spare_part.html', context)
