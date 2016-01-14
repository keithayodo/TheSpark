# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 03:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the forum.', max_length=50)),
                ('description', models.CharField(help_text='Description of the forum.', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='The Date & Time when this forum was created.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last time forum details were updated.')),
            ],
        ),
        migrations.CreateModel(
            name='ForumMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date of Time of message posting.')),
                ('message', models.CharField(help_text='Mesasge content.', max_length=1000)),
                ('relation', models.ForeignKey(help_text='Forum that message belongs to.', on_delete=django.db.models.deletion.CASCADE, to='forums.Forum')),
                ('sender', models.ForeignKey(help_text='Sender of the message', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(help_text='Message of reporter.', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the forum was reported.')),
                ('forum_relation', models.ForeignKey(help_text='Forum being reported.', on_delete=django.db.models.deletion.CASCADE, to='forums.Forum')),
                ('relation', models.ForeignKey(help_text='Spark user who is reporting a forum.', on_delete=django.db.models.deletion.CASCADE, to='users.SparkUser')),
            ],
        ),
        migrations.CreateModel(
            name='ForumRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_name', models.CharField(help_text='Proposed forum name.', max_length=50)),
                ('message', models.CharField(help_text='Message content.', max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time of forum request submission.')),
                ('relation', models.ForeignKey(help_text='Spark user requesting a new forum.', on_delete=django.db.models.deletion.CASCADE, to='users.SparkUser')),
            ],
        ),
        migrations.CreateModel(
            name='LastForumMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='First name of last message sender.', max_length=200)),
                ('last_name', models.CharField(help_text='Last name of last message sender.', max_length=200)),
                ('message', models.CharField(help_text='Last message sent in forum.', max_length=1000)),
                ('created_at', models.DateTimeField(help_text='Time when last message was sent in forum.')),
                ('relation', models.OneToOneField(help_text='Last/latest message sent in forum.', on_delete=django.db.models.deletion.CASCADE, to='forums.Forum')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forum_relation', models.ForeignKey(help_text='Forum which user is a member.', on_delete=django.db.models.deletion.CASCADE, to='forums.Forum')),
                ('user_relation', models.ForeignKey(help_text='User who has joined a forum.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('forum_relation', 'user_relation')]),
        ),
    ]
