# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lastconvomessage',
            name='last_name',
            field=models.CharField(default='N/A', help_text='Last Name of the sender', max_length=200),
        ),
        migrations.AlterField(
            model_name='lastconvomessage',
            name='first_name',
            field=models.CharField(help_text='First name of the sender', max_length=200),
        ),
    ]