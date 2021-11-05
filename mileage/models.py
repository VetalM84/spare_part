from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy


class CarBrand(models.Model):
    brand = models.CharField(max_length=40, choices=(), unique=True, verbose_name="Марка")

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse_lazy('car_models_all', kwargs={'car_id': self.pk})

    class Meta:
        verbose_name = 'Марка авто'
        verbose_name_plural = 'Марки авто'
        ordering = ['brand']


class CarModel(models.Model):
    model_name = models.CharField(max_length=60, db_index=True, verbose_name="Модель")
    brand_id = models.SmallIntegerField(verbose_name="ID марки")

    def __str__(self):
        return self.model_name

    def get_absolute_url(self):
        return reverse_lazy('model_info', kwargs={'model_id': self.pk})

    class Meta:
        verbose_name = 'Модель авто'
        verbose_name_plural = 'Модели авто'
        ordering = ['brand_id']


class SparePartCategory(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('spare_parts_category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория запчасти'
        verbose_name_plural = 'Категории запчастей'
        ordering = ['name']


class SparePart(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    brand = models.CharField(max_length=255, db_index=True, verbose_name="Производитель")
    number = models.CharField(max_length=30, db_index=True, verbose_name="Номер (артикул)")
    category = models.ForeignKey(SparePartCategory, on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return ' '.join([self.name, self.brand, self.number])

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['category', 'name']


class Review(models.Model):
    RATING_VALUES = [
        ('1', 'Ужасно'), ('2', 'Плохо'), ('3', 'Сносно'), ('4', 'Хорошо'), ('5', 'Отлично'),
    ]
    spare_part = models.ForeignKey(SparePart, on_delete=models.PROTECT, verbose_name="Запчасть")
    mileage = models.SmallIntegerField(verbose_name="Пробег, тыс.км")
    car_brand = models.ForeignKey(CarBrand, on_delete=models.PROTECT, verbose_name="Марка авто")
    car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, verbose_name="Модель авто")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    rating = models.CharField(max_length=1, choices=RATING_VALUES, verbose_name="Рейтинг", default=3)
    review = models.TextField(max_length=1000, blank=True, verbose_name="Отзыв")

    def __str__(self):
        return ' '.join([self.spare_part.name, self.spare_part.brand, self.spare_part.number])

    # def get_absolute_url(self):
    #     return reverse_lazy('user_profile_page', kwargs={'user_id': self.pk})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['spare_part']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    drive2_link = models.URLField(blank=True, verbose_name="Ссылка на профиль Drive2.ru")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse_lazy('user_profile_page', kwargs={'user_id': self.pk})

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
        ordering = ['id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
