# Generated by Django 3.2.8 on 2021-11-19 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mileage', '0011_alter_carbrand_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='media/avatar/default_avatar.jpg', upload_to='media/avatar/',
                                    verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='carbrand',
            name='logo',
            field=models.ImageField(blank=True, upload_to='media/logo/', verbose_name='Эмблема'),
        ),
    ]