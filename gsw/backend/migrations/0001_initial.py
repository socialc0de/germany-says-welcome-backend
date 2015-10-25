# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('translation', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='PhraseCollection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('english_phrase', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='phrases')),
            ],
        ),
        migrations.CreateModel(
            name='POI',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=200)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('county', models.IntegerField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='pois')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('question', models.CharField(max_length=200)),
                ('answer', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=2)),
                ('county', models.IntegerField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='questions')),
            ],
        ),
        migrations.AddField(
            model_name='phrase',
            name='collection',
            field=models.ForeignKey(to='backend.PhraseCollection', related_name='translations'),
        ),
        migrations.AddField(
            model_name='phrase',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='translations'),
        ),
    ]
