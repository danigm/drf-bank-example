# Generated by Django 2.2.4 on 2019-08-15 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iban', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iban',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='created_ibans', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
