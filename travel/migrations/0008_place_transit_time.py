# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_auto_20170205_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='transit_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
