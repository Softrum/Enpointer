# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-10 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dragonslayer', '0013_auto_20170910_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
