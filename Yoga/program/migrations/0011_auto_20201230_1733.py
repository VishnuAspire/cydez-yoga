# Generated by Django 3.1.1 on 2020-12-30 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0010_auto_20201230_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
    ]