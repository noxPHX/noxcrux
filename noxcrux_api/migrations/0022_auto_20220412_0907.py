# Generated by Django 3.2.12 on 2022-04-12 09:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noxcrux_api', '0021_userkeyscontainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkeyscontainer',
            name='iv',
            field=models.BinaryField(editable=True, max_length=12, validators=[django.core.validators.MinLengthValidator(12)]),
        ),
        migrations.AlterField(
            model_name='userkeyscontainer',
            name='private_key',
            field=models.BinaryField(editable=True),
        ),
        migrations.AlterField(
            model_name='userkeyscontainer',
            name='public_key',
            field=models.BinaryField(editable=True),
        ),
    ]
