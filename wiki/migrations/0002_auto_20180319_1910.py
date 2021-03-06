# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-19 19:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wiki.Version'),
        ),
        migrations.AlterField(
            model_name='history',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='wiki.Page'),
        ),
        migrations.AlterField(
            model_name='page',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='wiki.Category'),
        ),
    ]
