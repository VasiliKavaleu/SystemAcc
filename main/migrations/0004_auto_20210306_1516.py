# Generated by Django 3.1.7 on 2021-03-06 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210306_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='product',
        ),
        migrations.AddField(
            model_name='productonstorage',
            name='shops',
            field=models.ManyToManyField(blank=True, to='main.Shop', verbose_name='Магазины'),
        ),
    ]