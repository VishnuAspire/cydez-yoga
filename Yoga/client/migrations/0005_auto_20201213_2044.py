# Generated by Django 3.1.1 on 2020-12-13 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_auto_20201213_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='doctor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
