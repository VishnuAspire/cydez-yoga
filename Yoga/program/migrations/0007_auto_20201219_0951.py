# Generated by Django 3.1.4 on 2020-12-19 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0006_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='description',
        ),
        migrations.RemoveField(
            model_name='level',
            name='image',
        ),
        migrations.RemoveField(
            model_name='level',
            name='metakeywords',
        ),
    ]