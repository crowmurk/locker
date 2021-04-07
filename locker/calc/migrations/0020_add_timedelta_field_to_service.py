# Generated by Django 3.1.7 on 2021-04-03 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0019_split_service_price_to_equipment_and_work_price_on_orderoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='work_duration',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='Work duration'),
        ),
    ]
