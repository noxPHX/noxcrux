# Generated by Django 3.2.12 on 2022-04-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noxcrux_api', '0023_auto_20220412_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkeyscontainer',
            name='iv',
            field=models.CharField(max_length=255),
        ),
    ]