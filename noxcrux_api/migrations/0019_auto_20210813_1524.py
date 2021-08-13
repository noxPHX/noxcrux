# Generated by Django 3.2.4 on 2021-08-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noxcrux_api', '0018_usersession'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usersession',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
