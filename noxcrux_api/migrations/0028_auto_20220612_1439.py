# Generated by Django 3.2.13 on 2022-06-12 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('noxcrux_api', '0027_rename_private_key_userkeyscontainer_protected_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horcrux',
            name='grantees',
        ),
        migrations.CreateModel(
            name='SharedHorcrux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_horcrux', models.CharField(max_length=8192)),
                ('grantee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_horcruxes', to=settings.AUTH_USER_MODEL)),
                ('horcrux', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noxcrux_api.horcrux')),
            ],
        ),
    ]
