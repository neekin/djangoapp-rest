# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0003_auto_20171103_0052'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detail',
            unique_together=set([]),
        ),
    ]