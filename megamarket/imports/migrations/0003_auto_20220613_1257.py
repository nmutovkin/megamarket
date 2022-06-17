# Generated by Django 2.2.16 on 2022-06-13 12:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0002_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryOrOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('date', models.DateTimeField(verbose_name='Update date')),
                ('price', models.IntegerField(null=True, verbose_name='Price')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='imports.CategoryOrOffer')),
            ],
        ),
        migrations.RemoveField(
            model_name='offer',
            name='category_ptr',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
    ]
