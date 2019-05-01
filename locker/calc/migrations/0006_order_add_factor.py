# Generated by Django 2.2 on 2019-05-01 02:49

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0005_order_service_through_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='factor',
            field=models.FloatField(default=1, validators=[core.validators.validate_positive], verbose_name='Factor'),
        ),
    ]