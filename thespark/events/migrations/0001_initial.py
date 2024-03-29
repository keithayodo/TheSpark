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
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Time event was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Time event was last updated')),
                ('event_title', models.CharField(help_text='Title of the event.', max_length=100)),
                ('event_venue', models.CharField(help_text='Venue of the event.', max_length=50)),
                ('event_description', models.CharField(help_text='Description of the event.', max_length=300)),
                ('event_start_date_time', models.DateTimeField(help_text='Time and Date of event start.')),
                ('event_end_date_time', models.DateTimeField(help_text='Time and Date of event end.')),
                ('event_requires_rsvp', models.BooleanField(default=False, help_text='Indicates whether event requires an RSVP.')),
                ('rsvp_number', models.IntegerField(default=0, help_text='Show the number of people required to RSVP to event.')),
                ('is_showing', models.BooleanField(default=True, help_text='Indicates whether this event is viewable on the website.')),
                ('is_featured', models.BooleanField(default=False, help_text='Shows whether this is a featured event.')),
                ('event_views', models.IntegerField(default=0, editable=False, help_text='Counter for event views.')),
                ('relation', models.ForeignKey(help_text='Relation to any system who created this event.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(help_text="User's comment.", max_length=300)),
                ('created_at', models.DateTimeField(auto_now=True, help_text='Date & Time comment was made.')),
                ('event_relation', models.ForeignKey(help_text='Event being commented on.', on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user_relation', models.ForeignKey(help_text='User who is commenting on event.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Email of the reporter', max_length=254)),
                ('details', models.CharField(help_text='Contents of the report.', max_length=150)),
                ('created_at', models.DateTimeField(auto_now=True, help_text='Date & Time that report was made.')),
            ],
        ),
        migrations.CreateModel(
            name='EventRSVP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, help_text="Shows when the user RSVP'd.")),
                ('event_relation', models.ForeignKey(help_text="Event being RSVP'd to.", on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user_relation', models.ForeignKey(help_text="User instance who RSVP'd to event.", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Education', 'Education'), ('Technology', 'Technology'), ('Finance', 'Finance'), ('Agriculture', 'Agriculture')], help_text='Tag for an event.', max_length=50)),
                ('relation', models.ForeignKey(help_text='Event being tagged', on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='eventtag',
            unique_together=set([('relation', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='eventrsvp',
            unique_together=set([('user_relation', 'event_relation')]),
        ),
    ]
