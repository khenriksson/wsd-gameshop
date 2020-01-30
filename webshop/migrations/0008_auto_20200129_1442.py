# Generated by Django 3.0.2 on 2020-01-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0007_gamestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gameID', models.IntegerField()),
                ('username', models.CharField(max_length=40)),
                ('gameInfo', models.TextField()),
                ('score', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('gameID', 'username')},
            },
        ),
        migrations.DeleteModel(
            name='GameStatus',
        ),
    ]
