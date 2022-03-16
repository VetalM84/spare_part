import simplejson
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import Length
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import (AddReviewForm, AddSparePartForm, ProfileEditForm,
                    UserEditForm, UserLoginForm, UserRegisterForm)
from .models import (CarBrand, CarModel, Comment, Profile, Review, SparePart,
                     SparePartCategory, User)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'mileage/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'mileage/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@cache_page(30)
def index(request):
    """ получаем список всех марок авто на домашней странице"""
    cars = CarBrand.objects.all()
    context = {
        'cars': cars,
        'title': 'Список всех марок автомобилей',
    }
    return render(request, template_name='mileage/index.html', context=context)


@cache_page(30)
def get_car_models(request, car_id):
    """ получаем список моделей авто """
    car_brand = CarBrand.objects.get(pk=car_id)
    # получаем и выводим кол-во отзывов к маркам авто
    car_models = CarModel.objects.filter(brand_id=car_id).order_by('model_name').annotate(cnt=Count('review'))

    context = {
        'car_brand': car_brand,
        'car_models': car_models,
        'title': 'Все модели',
    }
    return render(request, 'mileage/car_models.html', context)


def get_model_info(request, model_id):
    """ получаем информацию о конкретной модели авто """
    car_model = CarModel.objects.get(pk=model_id)
    car_brand = CarBrand.objects.get(pk=car_model.brand_id)
    # отображаем только уникальные запчасти у которых есть отзыв к этой модели
    spare_parts = Review.objects.filter(car_model_id=model_id).order_by('spare_part__name')\
        .distinct('spare_part__name', 'spare_part__brand', 'spare_part__number').select_related('spare_part')
    context = {
        'spare_parts': spare_parts,
        'car_model': car_model,
        'car_brand': car_brand,
        'title': f'Все для {car_brand.brand} {car_model.model_name}',
    }
    return render(request, 'mileage/model_info.html', context)


def get_spare_parts_category(request, category_id):
    """ выводим список запчастей в определенной категории """
    all_spare_parts = SparePart.objects.filter(category_id=category_id).order_by('name', 'brand').\
        annotate(cnt=Count('review'))
    category_name = SparePartCategory.objects.get(pk=category_id)
    context = {
        'category_name': category_name,
        'all_spare_parts': all_spare_parts,
    }
    return render(request, 'mileage/spare_parts_category.html', context)


def get_all_spare_parts_categories(request):
    """ выводим список всех категорий автозапчастей """
    # кешируем запрос
    categories = cache.get('categories')
    if not categories:
        categories = SparePartCategory.objects.all().order_by('pk').annotate(cnt=Count('sparepart'))
        cache.set('categories', categories, 30)
    context = {
        'title': 'Все категории запчастей',
        'categories': categories,
    }
    return render(request, 'mileage/all_spare_parts_categories.html', context)


@login_required
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
    spare_parts_names = SparePart.objects.order_by('name').distinct('name')
    spare_parts_brands = SparePart.objects.order_by('brand').distinct('brand')
    context = {
        'title': 'Добавить новую запчасть в каталог',
        'form': form,
        'spare_parts_names': spare_parts_names,
        'spare_parts_brands': spare_parts_brands,
    }
    return render(request, 'mileage/add_new_spare_part.html', context)


def get_model_spare_parts_reviews(request, model_id, spare_part_id):
    """ получаем список всех записей о пробеге для конкретной запчасти на конкретной марке и модели авто """
    spare_part = SparePart.objects.get(pk=spare_part_id)
    car_model = CarModel.objects.get(pk=model_id)
    car_brand = CarBrand.objects.get(pk=car_model.brand_id)
    spare_parts = Review.objects.filter(car_model_id=model_id, spare_part_id=spare_part_id).order_by('-mileage').\
        select_related('car_brand', 'car_model', 'owner')
    max_mileage = spare_parts.aggregate(Max('mileage'))
    min_mileage = spare_parts.aggregate(Min('mileage'))
    avg_mileage = spare_parts.aggregate(Avg('mileage'))
    avg_rating = spare_parts.aggregate(Avg('rating'))
    records_count = spare_parts.count()

    # TODO искючить из выдачи текущую запчасть
    # список похожих запчастей по имени запчасти c учетом модели авто
    similar_spare_parts = Review.objects.filter(
        spare_part__name__icontains=spare_part.name, spare_part__category_id=spare_part.category.id,
        car_model__id=model_id).order_by('spare_part__name', 'spare_part__brand', 'spare_part__number').\
        distinct('spare_part__name', 'spare_part__brand', 'spare_part__number').\
        select_related('spare_part')
    # similar_spare_parts = Review.objects.filter(spare_part__name__icontains=spare_parts.first().
    #                                             spare_part.name).exclude(spare_part_id=spare_part_id)
    context = {
        'car_brand': car_brand,
        'car_model': car_model,
        'spare_part': spare_part,
        'spare_parts': spare_parts,
        'similar_spare_parts': similar_spare_parts,
        'title': 'Отзывы для запчасти',
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'avg_rating': avg_rating['rating__avg'],
        'records_count': records_count,
    }
    return render(request, 'mileage/spare_part_by_car.html', context)


@login_required
def get_private_user_profile(request):
    """ отображаем личный профиль пользователя """
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()

    user_reviews = Review.objects.filter(owner_id=request.user.id).order_by('spare_part', 'spare_part__category_id')\
        .select_related('spare_part')
    # user_liked = Review.objects.filter(likes=request.user)

    paginator = Paginator(user_reviews, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        # 'user_liked': user_liked,
        'page_obj': page_obj,
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Мой профиль',
    }
    return render(request, 'mileage/user_profile.html', context)


def get_public_user_profile(request, user_id):
    """ отображаем публичный профиль пользователя """
    user = get_object_or_404(Profile, pk=user_id)
    user_reviews = Review.objects.filter(owner_id=user.id).order_by('spare_part', 'spare_part__category_id').\
        select_related('spare_part')

    paginator = Paginator(user_reviews, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'Публичный профиль пользователя',
        'profile': user,
        'user_reviews': user_reviews,
    }
    return render(request, 'mileage/user_public_profile.html', context)


@login_required
def add_review(request):
    """ добавляем отзыв """
    user_id = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        review_form = AddReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            # назначаем полю owner id пользователя, который залогинился
            review_form = review_form.save(commit=False)
            review_form.owner = user_id
            review_form.save()
            messages.success(request, 'Отзыв успешно опубликован!')
            # редирект на страницу запчасти
            return redirect('get_spare_part', spare_part_id=request.POST.get('spare_part'))
    else:
        review_form = AddReviewForm()

    # для автокомплита
    spare_parts = SparePart.objects.all().distinct()

    context = {
        'title': 'Добавить отзыв о запчасти',
        'review_form': review_form,
        'spare_parts': spare_parts,
    }
    return render(request, 'mileage/add_review.html', context)


def search(request):
    """ поиск по названию или номеру запчасти """
    query, search_result = '', []
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            search_result = SparePart.objects.filter(Q(name__icontains=query) | Q(number__icontains=query)).\
                annotate(cnt=Count('review'))
        else:
            query = ''
            search_result = []

    paginator = Paginator(search_result, 15)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'title': 'Результаты поиска по запросу',
        'query': query,
        'search_result': search_result,
    }
    return render(request, 'mileage/search.html', context)


def get_spare_part(request, spare_part_id):
    """ вся информация о запчасти """
    spare_part = get_object_or_404(SparePart, pk=spare_part_id)

    # список пробегов запчасти
    spare_parts_reviews = Review.objects.filter(spare_part_id=spare_part_id)\
        .order_by('-date', '-like_count', Length('testimonial').desc())\
        .select_related('car_brand', 'car_model', 'owner')
    # или такой запрос
    # spare_parts_reviews = spare_part.review_set.all().order_by('-mileage')

    max_mileage = spare_parts_reviews.aggregate(Max('mileage'))
    min_mileage = spare_parts_reviews.aggregate(Min('mileage'))
    avg_mileage = spare_parts_reviews.aggregate(Avg('mileage'))
    avg_rating = spare_parts_reviews.aggregate(Avg('rating'))
    records_count = spare_parts_reviews.count()

    # список авто, где стоит эта запчасть
    cars = spare_part.review_set.all().order_by('car_brand__brand', 'car_model__model_name').\
        distinct('car_brand__brand', 'car_model__model_name').select_related('car_brand', 'car_model')

    paginator = Paginator(spare_parts_reviews, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'spare_part': spare_part,
        'min_mileage': min_mileage['mileage__min'],
        'max_mileage': max_mileage['mileage__max'],
        'avg_mileage': avg_mileage['mileage__avg'],
        'avg_rating': avg_rating['rating__avg'],
        'records_count': records_count,
        # 'spare_parts_reviews': spare_parts_reviews,
        'cars': cars,
    }
    return render(request, 'mileage/spare_part.html', context)


def get_chained_car_models(request, brand_id):
    """ получаем связанный список брендов и моделей авто """
    car_brand = CarBrand.objects.get(pk=brand_id)
    car_models = CarModel.objects.filter(brand_id=car_brand.id)
    models_dict = {}
    for item in car_models:
        models_dict[item.id] = item.model_name
    return HttpResponse(simplejson.dumps(models_dict), content_type="application/json")


class SparePartAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return SparePart.objects.none()
        spare_parts_list = SparePart.objects.all()
        if self.q:
            spare_parts_list = spare_parts_list.filter(name__istartswith=self.q)
        return spare_parts_list


# class CarBrandAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         if not self.request.user.is_authenticated:
#             return CarBrand.objects.none()
#         car_brands_list = CarBrand.objects.all()
#         if self.q:
#             car_brands_list = car_brands_list.filter(brand__istartswith=self.q)
#         return car_brands_list


def like(request):
    """ лайки к отзывам """
    if request.POST.get('action') == 'post':
        review_id = int(request.POST.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        if review.likes.filter(id=request.user.id).exists():
            review.likes.remove(request.user)
            review.like_count -= 1
            result = review.like_count
            review.save()
        else:
            review.likes.add(request.user)
            review.like_count += 1
            result = review.like_count
            review.save()
        return JsonResponse({'result': result, })


def add_comment(request):
    """ комментарии к отзывам """
    if request.POST.get('action') == 'post':
        review_id = int(request.POST.get('review_id'))
        review = get_object_or_404(Review, id=review_id)
        comment_text = request.POST.get('comment_text')
        if request.user.is_authenticated:
            if len(comment_text) > 20:
                comment = Comment.objects.create(user=request.user, review=review, comments_text=comment_text)
                result = review.comment.all().count()
                comment.save()
                message = 'Отзыв добавлен!'
            else:
                result = ''
                message = 'Ошибка! Введите минимум 20 символов.'
        else:
            result = ''
            message = 'Войдите, чтобы оставить комментарий'
        return JsonResponse({'result': result, 'message': message})
