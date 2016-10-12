# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 07:46
from __future__ import unicode_literals

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
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('acronym', models.CharField(blank=True, max_length=20, null=True, verbose_name='Acronyme')),
                ('description', models.TextField(verbose_name='Description')),
                ('is_validated', models.BooleanField(default=False, verbose_name='Est validée')),
                ('has_place', models.BooleanField(default=False, verbose_name='Possède un local?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'admin'),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('position', models.IntegerField(blank=True, verbose_name='Position')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'admin'),
            },
        ),
        migrations.AddField(
            model_name='association',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.Category', verbose_name='Catégorie'),
        ),
        migrations.AddField(
            model_name='association',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateurs'),
        ),
    ]
