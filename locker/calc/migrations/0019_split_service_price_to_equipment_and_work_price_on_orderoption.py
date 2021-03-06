# Generated by Django 2.2.7 on 2019-11-16 18:07

from decimal import Decimal, ROUND_HALF_UP

from django.db import migrations, models


def calc_price(apps, schema_editor):
    OrderOption = apps.get_model('calc', 'OrderOption')

    for option in OrderOption.objects.all():
        option.equipment_price = option.service.equipment_price
        work_price = option.service.work_price * Decimal(option.order.factor)
        option.work_price = work_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        option.price = (option.equipment_price + option.work_price) * option.quantity
        option.save()


def calc_price_reverse(apps, schema_editor):
    OrderOption = apps.get_model('calc', 'OrderOption')

    for option in OrderOption.objects.all():
        service_price = option.service.equipment_price + option.service.work_price * Decimal(option.order.factor)
        option.service_price = service_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        option.price = option.service_price * option.quantity
        option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0018_change_verbose_name_for_work_on_service'),
    ]

    operations = [
        migrations.RunPython(
            migrations.RunPython.noop,
            reverse_code=calc_price_reverse,
        ),
        migrations.RemoveField(
            model_name='orderoption',
            name='service_price',
        ),
        migrations.AddField(
            model_name='orderoption',
            name='equipment_price',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=9, verbose_name='Equipment price'),
        ),
        migrations.AddField(
            model_name='orderoption',
            name='work_price',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=9, verbose_name='Work price'),
        ),
        migrations.RunPython(
            calc_price,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
