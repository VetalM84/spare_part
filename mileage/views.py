from django.shortcuts import render, redirect
from django.db.models import Avg, Max, Min, Q, Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

import simplejson

from .models import Review, CarModel, CarBrand, SparePart, SparePartCategory
from .forms import AddCarBrandForm, AddCarModelForm, AddReviewForm, AddSparePartForm


def index(request):
    """ получаем список всех марок авто на домашней странице"""
    cars = CarBrand.objects.all()
    context = {
        'cars': cars,
        'title': 'Список всех марок автомобилей',
    }
    return render(request, template_name='mileage/index.html', context=context)


def get_car_models(request, car_id):
    """ получаем список моделей авто """
    car_brand = CarBrand.objects.get(pk=car_id)
    # получаем и выводим кол-во отзывов к маркам авто
    car_models = CarModel.objects.filter(brand_id=car_id).annotate(cnt=Count('review'))

    context = {
        'car_models': car_models,
        'title': f'Все модели {car_brand}',
    }
    return render(request, 'mileage/car_models.html', context)


def get_model_info(request, model_id):
    """ получаем информацию о конкретной модели авто """
    car_model = CarModel.objects.get(pk=model_id)
    car_brand = CarBrand.objects.get(pk=car_model.brand_id)
    spare_parts = Review.objects.filter(car_model_id=model_id)
    context = {
        'spare_parts': spare_parts,
        'car_model': car_model,
        'car_brand': car_brand,
        'title': f'Все для {car_brand.brand} {car_model.model_name}',
    }
    return render(request, 'mileage/model_info.html', context)


def get_spare_parts_category(request, category_id):
    """ выводим список запчастей в определенной категории """
    all_spare_parts = SparePart.objects.filter(category_id=category_id)
    category_name = SparePartCategory.objects.get(pk=category_id)
    context = {
        'title': category_name,
        'all_spare_parts': all_spare_parts,
    }
    return render(request, 'mileage/spare_parts_category.html', context)


def get_all_spare_parts_categories(request):
    """ выводим список всех категорий автозапчастей """
    categories = SparePartCategory.objects.all().order_by('pk').annotate(cnt=Count('sparepart'))
    context = {
        'title': 'Все категории запчастей',
        'categories': categories,
    }
    return render(request, 'mileage/all_spare_parts_categories.html', context)


def add_new_spare_part(request):
    """ добавляем новую запчасть в каталог """
    if request.method == 'POST':
        form = AddSparePartForm(request.POST)
        s_p_name = request.POST.get('name')
        s_p_brand = request.POST.get('brand')
        s_p_number = request.POST.get('number')
        if form.is_valid():
            # если такая запчасть существует, то не плодим дубли
            try:
                SparePart.objects.get(name__iexact=s_p_name, brand__iexact=s_p_brand, number__iexact=s_p_number)
                messages.error(request, 'Такая запчасть уже существует')
            except SparePart.DoesNotExist:
                form.save()
                messages.success(request, 'Запчасть успешно добавлена в каталог')
                return redirect('add_review_page')
    else:
        form = AddSparePartForm()

    # для автокомплита
    spare_parts = SparePart.objects.all().distinct()

    context = {
        'title': 'Добавить новую запчасть в каталог',
        'form': form,
        'spare_parts': spare_parts,
    }
    return render(request, 'mileage/add_new_spare_part.html', context)


def get_model_spare_parts_reviews(request, model_id, spare_part_id):
    """ получаем список всех записей о пробеге для конкретной запчасти на конкретной марке и модели авто """
    spare_parts = Review.objects.filter(car_model_id=model_id, spare_part_id=spare_part_id).order_by('-mileage')
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
        # 'brand': car.brand,
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'avg_rating': avg_rating['rating__avg'],
        'records_count': records_count,
    }
    return render(request, 'mileage/spare_part_by_car.html', context)


def get_user_profile(request, user_id):
    user_reviews = Review.objects.filter(owner_id=user_id).order_by('spare_part', 'spare_part__category_id')
    context = {
        'title': 'Мой профиль',
        'user_reviews': user_reviews
    }
    return render(request, 'mileage/user_profile.html', context)


def get_chained_car_models(request, brand_id):
    """ получаем связанный список брендов и моделей авто """
    car_brand = CarBrand.objects.get(pk=brand_id)
    car_models = CarModel.objects.filter(brand_id=car_brand.id)
    models_dict = {}
    for item in car_models:
        models_dict[item.id] = item.model_name
    return HttpResponse(simplejson.dumps(models_dict), content_type="application/json")


def add_review(request):
    """ добавляем отзыв """
    if request.method == 'POST':
        # car_form = AddCarBrandForm(request.POST)
        # model_form = AddCarModelForm(request.POST)
        # spare_part_form = AddSparePartForm(request.POST)
        review_form = AddReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect('home')
    else:
        # car_form = AddCarBrandForm()
        # model_form = AddCarModelForm()
        review_form = AddReviewForm()
        # spare_part_form = AddSparePartForm()

    # для автокомплита
    spare_parts = SparePart.objects.all().distinct()

    context = {
        'title': 'Добавить отзыв о запчасти',
        # 'car_form': car_form,
        # 'model_form': model_form,
        # 'spare_part_form': spare_part_form,
        'review_form': review_form,
        'spare_parts': spare_parts,
    }
    return render(request, 'mileage/add_review.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            search_result = SparePart.objects.filter(Q(name__icontains=query) | Q(number__icontains=query))
        else:
            query = ''
            search_result = []
    context = {
        'title': 'Результаты поиска по запросу',
        'query': query,
        'search_result': search_result,
    }
    return render(request, 'mileage/search.html', context)


def get_spare_part(request, spare_part_id):
    spare_part = get_object_or_404(SparePart, pk=spare_part_id)

    spare_parts_mileages = Review.objects.filter(spare_part_id=spare_part_id).order_by('-mileage')
    # spare_parts_mileages = spare_part.review_set.all().order_by('-mileage')
    max_mileage = spare_parts_mileages.aggregate(Max('mileage'))
    min_mileage = spare_parts_mileages.aggregate(Min('mileage'))
    avg_mileage = spare_parts_mileages.aggregate(Avg('mileage'))
    avg_rating = spare_parts_mileages.aggregate(Avg('rating'))
    records_count = spare_parts_mileages.count()

    cars = spare_part.review_set.all()
    # reviews = spare_part.review_set.all()
    # unique_brands = CarBrand.objects.filter(review__in=reviews).distinct()
    # unique = CarModel.objects.filter(review__in=reviews).distinct()

    context = {
        # 'unique_brands': unique_brands,
        # 'unique': unique,
        'spare_part': spare_part,
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'avg_rating': avg_rating['rating__avg'],
        'records_count': records_count,
        'spare_parts_mileages': spare_parts_mileages,
        'cars': cars,
    }
    return render(request, 'mileage/spare_part.html', context)
