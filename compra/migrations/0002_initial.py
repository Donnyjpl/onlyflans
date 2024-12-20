# Generated by Django 3.2 on 2024-10-15 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('compra', '0001_initial'),
        ('web', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carritoflan',
            name='flan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.flan'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='flanes',
            field=models.ManyToManyField(through='compra.CarritoFlan', to='web.Flan'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
