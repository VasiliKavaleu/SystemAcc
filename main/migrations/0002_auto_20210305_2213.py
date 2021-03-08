# Generated by Django 3.1.7 on 2021-03-05 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='shop',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sold',
        ),
        migrations.RemoveField(
            model_name='product',
            name='storage',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='slug',
        ),
        migrations.AddField(
            model_name='shop',
            name='product',
            field=models.ManyToManyField(to='main.Product', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='main.category'),
        ),
        migrations.CreateModel(
            name='SoldProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_products', to='main.product')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_products', to='main.shop')),
                ('storage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sold_products', to='main.storage')),
            ],
            options={
                'verbose_name': 'Проданный товар',
                'verbose_name_plural': 'Проданные товары',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductOnStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=False, verbose_name='Наличие на складе')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.product', verbose_name='Товар')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.storage', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Наличие товара на складе',
                'verbose_name_plural': 'Наличие товаров на складе',
            },
        ),
    ]