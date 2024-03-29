# Generated by Django 3.2.8 on 2021-10-10 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=40, verbose_name='Марка')),
                ('model_name', models.CharField(max_length=60, verbose_name='Модель')),
                ('model_variant', models.CharField(max_length=100, verbose_name='Модификация')),
                ('age', models.SmallIntegerField(verbose_name='Год выпуска')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
                'ordering': ['brand'],
            },
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('brand', models.CharField(max_length=255, verbose_name='Производитель')),
                ('number', models.CharField(max_length=30, unique=True, verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Запчасть',
                'verbose_name_plural': 'Запчасти',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mileage', models.SmallIntegerField(verbose_name='Пробег')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mileage.car', verbose_name='Автомобиль')),
                ('spare_part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mileage.sparepart', verbose_name='Запчасть')),
            ],
            options={
                'verbose_name': 'Пробег',
                'verbose_name_plural': 'Пробег',
            },
        ),
    ]
