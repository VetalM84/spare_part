# Generated by Django 3.2.8 on 2021-10-30 08:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mileage', '0006_auto_20211029_1323'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mileage',
            new_name='Review',
        ),
    ]
