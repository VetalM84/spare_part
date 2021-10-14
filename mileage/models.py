from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Car(models.Model):
    brand = models.CharField(max_length=40, db_index=True, verbose_name="Марка")
    model_name = models.CharField(max_length=60, db_index=True, verbose_name="Модель")
    model_variant = models.CharField(max_length=100, db_index=True, verbose_name="Модификация")
    age = models.SmallIntegerField(verbose_name="Год выпуска")

    def __str__(self):
        return ' '.join([self.brand, self.model_name, self.model_variant])

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['brand']


class SparePart(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    brand = models.CharField(max_length=255, db_index=True, verbose_name="Производитель")
    number = models.CharField(max_length=30, db_index=True, unique=True, verbose_name="Номер")

    def __str__(self):
        return ' '.join([self.name, self.brand, self.number])

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['name']


class Mileage(models.Model):
    spare_part = models.ForeignKey('SparePart', on_delete=models.PROTECT, verbose_name="Запчасть")
    car = models.ForeignKey('Car', on_delete=models.PROTECT, verbose_name="Автомобиль")
    mileage = models.SmallIntegerField(verbose_name="Пробег, тыс.км")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return ' '.join([self.spare_part.name, self.spare_part.brand, self.spare_part.number])

    class Meta:
        verbose_name = 'Пробег'
        verbose_name_plural = 'Пробег'
        ordering = ['spare_part']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nikname = models.CharField(max_length=30, verbose_name="Никнейм")
    drive2_link = models.URLField(blank=True, verbose_name="Ссылка на профиль Drive2.ru")
    cars = models.ManyToManyField(Car, blank=True, verbose_name="Мои автомобили")

    def __str__(self):
        return self.nikname

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
