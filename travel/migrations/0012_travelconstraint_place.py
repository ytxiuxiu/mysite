# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_auto_20170205_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelconstraint',
            name='place',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='travel.Place'),
            preserve_default=False,
        ),
    ]
