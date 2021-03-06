# Generated by Django 2.2.16 on 2022-06-13 12:04

import uuid

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
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('date', models.DateTimeField(verbose_name='Update date')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('category_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='imports.Category')),
                ('price', models.IntegerField(verbose_name='Price')),
            ],
            bases=('imports.category',),
        ),
    ]
