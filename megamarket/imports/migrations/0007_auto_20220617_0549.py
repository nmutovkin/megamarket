# Generated by Django 2.2.16 on 2022-06-17 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imports', '0006_auto_20220617_0541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryoroffer',
            options={'ordering': ['type', 'name'], 'verbose_name': 'Entity', 'verbose_name_plural': 'Entities'},
        ),
    ]
