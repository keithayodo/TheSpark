# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 03:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(help_text='User email address.', max_length=254, unique=True)),
                ('first_name', models.CharField(help_text='User first name.', max_length=50)),
                ('last_name', models.CharField(help_text='User last name.', max_length=50)),
                ('occupation', models.CharField(help_text='User occupation.', max_length=50)),
                ('phone_number', models.CharField(blank=True, help_text='User mobile number.', max_length=15, null=True)),
                ('show_email', models.BooleanField(default=False, help_text='If user allows public email address.')),
                ('show_number', models.BooleanField(default=False, help_text='If user allows public phone number.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CounsellorUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.OneToOneField(help_text='Connect a Counsellor to a user account.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SparkUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, help_text='Optional description about this user.', max_length=200, null=True)),
                ('fb_link', models.URLField(blank=True, help_text="Optional link to user's fb profile.", null=True)),
                ('twitter_link', models.URLField(blank=True, help_text="Optional link to user's twitter profile.", null=True)),
                ('relation', models.OneToOneField(help_text='Connect a spark user to a user account.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccomplishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accomplishment_title', models.CharField(help_text='Accomplishment title.', max_length=50)),
                ('accomplishment_summary', models.CharField(help_text='Accomplishment summary.', max_length=200)),
                ('start_date', models.DateField(help_text='Date when this accomplishment began.')),
                ('end_date', models.DateField(help_text='Date when this accomplishment ended.')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and Time when this accomplishment was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time accomplishment last updated.')),
                ('relation', models.ForeignKey(help_text='Spark user creating the accomplishment.', on_delete=django.db.models.deletion.CASCADE, to='users.SparkUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccomplishmentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Education', 'Education'), ('Technology', 'Technology'), ('Finance', 'Finance'), ('Agriculture', 'Agriculture')], help_text='Category of tag.', max_length=50)),
                ('relation', models.ForeignKey(help_text='Accomplishment being tagged.', on_delete=django.db.models.deletion.CASCADE, to='users.UserAccomplishment')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='useraccomplishmenttag',
            unique_together=set([('relation', 'category')]),
        ),
    ]
