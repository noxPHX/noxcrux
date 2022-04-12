# Generated by Django 3.2.12 on 2022-04-11 15:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('noxcrux_api', '0020_usersession_expire_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKeysContainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.BinaryField()),
                ('private_key', models.BinaryField()),
                ('iv', models.BinaryField(max_length=12, validators=[django.core.validators.MinLengthValidator(12)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
