# Generated by Django 5.1.1 on 2024-10-09 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, verbose_name='სახელი')),
                ('category_description', models.TextField(blank=True, null=True, verbose_name='აღწერა')),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='ზეკატეგორია')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='სახელი')),
                ('product_price', models.FloatField(verbose_name='ფასი')),
                ('product_description', models.TextField(blank=True, null=True, verbose_name='აღწერა')),
                ('product_image', models.ImageField(blank=True, help_text='ატვირთეთ ფოტოსურათი', null=True, upload_to='', verbose_name='სურათი')),
                ('product_category', models.ManyToManyField(to='store.category', verbose_name='კატეგორია')),
            ],
        ),
    ]
