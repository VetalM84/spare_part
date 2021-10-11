from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=40, verbose_name="Марка")
    model_name = models.CharField(max_length=60, verbose_name="Модель")
    model_variant = models.CharField(max_length=100, verbose_name="Модификация")
    age = models.SmallIntegerField(verbose_name="Год выпуска")

    def __str__(self):
        return ' '.join([self.brand, self.model_name, self.model_variant])

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['brand']


class SparePart(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    brand = models.CharField(max_length=255, verbose_name="Производитель")
    number = models.CharField(max_length=30, unique=True, verbose_name="Номер")

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

    def __str__(self):
        return ' '.join([self.spare_part.name, self.spare_part.brand, self.spare_part.number])

    class Meta:
        verbose_name = 'Пробег'
        verbose_name_plural = 'Пробег'
        ordering = ['spare_part']
