# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-10 12:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20160109_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lastconvomessage',
            old_name='full_name',
            new_name='first_name',
        ),
    ]
