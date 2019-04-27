# Generated by Django 2.2 on 2019-04-25 05:50

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(editable=False, help_text='A label for URL config.', max_length=120, validators=[core.validators.validate_slug])),
                ('details', models.CharField(help_text='Details regarding the client', max_length=500, verbose_name='Details')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
            },
        ),
    ]