# Generated by Django 2.2.7 on 2019-11-16 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0017_change_verbose_names_order_to_estimate_service_and_option_to_equipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='work',
            field=models.CharField(max_length=250, verbose_name='Work type'),
        ),
    ]
