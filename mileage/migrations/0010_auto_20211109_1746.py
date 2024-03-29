# Generated by Django 3.2.8 on 2021-11-09 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0009_auto_20211031_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbrand',
            name='logo',
            field=models.ImageField(blank=True, upload_to='logos/', verbose_name="Эмблема"),
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='brand',
            field=models.CharField(choices=[], max_length=40, unique=True, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='testimonial',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Отзыв'),
        ),
    ]
