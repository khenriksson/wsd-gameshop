# Generated by Django 3.0.2 on 2020-02-12 14:38

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_url', models.URLField()),
                ('picture_url', models.URLField(blank=True, default='https://store-images.s-microsoft.com/image/apps.58949.14571142807322667.df9fc94b-3bd3-4ec2-b7a2-423331d84b17.5883e11e-8555-4114-83b7-72d1cb12cd6e?mode=scale&q=90&h=1080&w=1920')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('game_title', models.CharField(default='Untitled', max_length=50)),
                ('description', models.CharField(default='', max_length=1000)),
                ('times_bought', models.PositiveIntegerField(default=0)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.IntegerField()),
                ('user', models.TextField()),
                ('gameInfo', models.TextField()),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_id', models.CharField(max_length=16, unique=True)),
                ('wallet_amount', models.FloatField(max_length=8)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('is_developer', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(default='Pending', max_length=20)),
                ('buy_started', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('buy_completed', models.DateTimeField(null=True)),
                ('pid', models.CharField(blank=True, max_length=64)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.Game')),
            ],
            options={
                'unique_together': {('game', 'buyer', 'pid')},
            },
        ),
    ]
