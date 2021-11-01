# Generated by Django 3.2.8 on 2021-10-31 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0007_rename_mileage_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carbrand',
            name='brand',
            field=models.CharField(choices=[], db_index=True, max_length=40, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='sparepart',
            name='number',
            field=models.CharField(db_index=True, max_length=30, verbose_name='Номер (артикул)'),
        ),
    ]
