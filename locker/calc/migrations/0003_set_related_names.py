# Generated by Django 2.2 on 2019-04-27 03:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_replace_authtor_by_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderoption',
            options={'verbose_name': 'Order option', 'verbose_name_plural': 'Orders options'},
        ),
        migrations.AlterField(
            model_name='order',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='client.Client', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='orderoption',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='calc.Order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='orderoption',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='calc.Service', verbose_name='Service'),
        ),
    ]
