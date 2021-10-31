from django.shortcuts import render
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404

from .models import Review, CarModel, CarBrand, SparePart, SparePartCategory
from .forms import AddCarForm, AddReviewForm, AddSparePartForm, AddCarModelForm


def index(request):
    """ получаем список всех марок авто """
    cars = CarBrand.objects.all()
    context = {
        'cars': cars,
        'title': 'Список всех марок автомобилей',
    }
    return render(request, template_name='mileage/index.html', context=context)


def get_car_models(request, car_id):
    """ получаем список моделей авто """
    car_brand = CarBrand.objects.get(pk=car_id)
    car_models = CarModel.objects.filter(brand_id=car_id)
    context = {
        'car_models': car_models,
        'title': f'Все модели {car_brand}',
    }
    return render(request, 'mileage/car_models.html', context)


def get_model_info(request, model_id):
    """ получаем информацию о конкретной модели авто """
    car_model = CarModel.objects.get(pk=model_id)
    car_brand = CarBrand.objects.get(pk=car_model.brand_id)
    context = {
        'car_model': car_model,
        'car_brand': car_brand,
        'title': f'Все для {car_brand.brand} {car_model.model_name}',
    }
    return render(request, 'mileage/model_info.html', context)


# def get_car_spare_parts(request, car_id):
#     """ получаем список запчастей для конкретной марки и модели авто """
#     spare_parts = Mileage.objects.filter(car_id=car_id).distinct()
#     # car = get_object_or_404(Car, pk=car_id)
#     context = {
#         'spare_parts': spare_parts,
#         'title': 'Список запчастей для',
#         # 'model_name': car.model_name,
#         # 'brand': car.brand,
#     }
#     return render(request, 'mileage/car.html', context)


def get_spare_parts_category(request, category_id):
    all_spare_parts = SparePart.objects.filter(category_id=category_id)
    category_name = SparePartCategory.objects.get(pk=category_id)
    context = {
        'title': category_name,
        'all_spare_parts': all_spare_parts,
    }
    return render(request, 'mileage/spare_parts_category.html', context)


def get_spare_parts_reviews(request, model_id, spare_part_id):
    """ получаем список всех записей о пробеге для конкретной запчасти на конкретной марке и модели авто """
    spare_parts = Review.objects.filter(car_id=model_id, spare_part_id=spare_part_id).order_by('-mileage')
    max_mileage = spare_parts.aggregate(Max('mileage'))
    min_mileage = spare_parts.aggregate(Min('mileage'))
    avg_mileage = spare_parts.aggregate(Avg('mileage'))
    avg_rating = spare_parts.aggregate(Avg('rating'))
    records_count = spare_parts.count()

    # car = get_object_or_404(Car, pk=car_id)
    # список похожих запчастей по имени запчасти исключая текущую
    # current_spare_part_name = SparePart.objects.get(id=spare_part_id).name
    # similar_spare_parts = SparePart.objects.filter(name__contains=current_spare_part_name)
    similar_spare_parts = Review.objects.filter(car_id=model_id, spare_part__name__icontains=spare_parts.first().
                                                spare_part.name).exclude(spare_part_id=spare_part_id)

    context = {
        'spare_parts': spare_parts,
        'similar_spare_parts': similar_spare_parts,
        'title': 'Список пробегов запчасти',
        # 'model_name': car.model_name,
        # 'model_generation': car.generation,
        # 'brand': car.brand,
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'avg_rating': avg_rating['rating__avg'],
        'records_count': records_count,
    }
    return render(request, 'mileage/spare_part.html', context)


def get_user_profile(request, user_id):
    user_reports = Review.objects.filter(owner_id=user_id)
    context = {
        'title': 'Мой профиль',
        'user_reports': user_reports
    }
    return render(request, 'mileage/user_profile.html', context)


def add_mileage(request):
    if request.method == 'POST':
        car_form = AddCarForm(request.POST)
        model_form = AddCarModelForm(request.POST)
        spare_part_form = AddSparePartForm(request.POST)
        # mileage_form = AddMileageForm(request.POST)
    else:
        car_form = AddCarForm()
        model_form = AddCarModelForm()
        spare_part_form = AddSparePartForm()
        # mileage_form = AddMileageForm()

    spare_parts = SparePart.objects.distinct()

    context = {
        'title': 'Добавить отчет о пробеге',
        'car_form': car_form,
        'model_form': model_form,
        'spare_part_form': spare_part_form,
        # 'mileage_form': mileage_form,
        'spare_parts': spare_parts,
    }
    return render(request, 'mileage/add_mileage.html', context)


def load_models(request):
    car_brand_id = request.GET.get('car_brand_id')
    car_models = CarModel.objects.filter(brand_id=car_brand_id).order_by('model_name')
    print(f'GET car_brand_id: {car_brand_id}')
    print(f'car models: {car_models}')
    return render(request, 'mileage/car_models_dropdown_list.html', {'car_models': car_models})
