# Generated by Django 3.0.2 on 2020-01-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0005_game_picture_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.CharField(default='Default description', max_length=1000),
            preserve_default=False,
        ),
    ]
