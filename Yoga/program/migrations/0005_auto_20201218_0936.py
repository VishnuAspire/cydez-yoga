# Generated by Django 3.1.4 on 2020-12-18 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0004_auto_20201218_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='description',
            field=models.TextField(max_length=100, null=True),
        ),
    ]
