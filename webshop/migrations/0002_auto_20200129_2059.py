# Generated by Django 2.2.7 on 2020-01-29 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='webshop.User'),
        ),
    ]