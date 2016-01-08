from __future__ import unicode_literals

from django.db import models

# Create your models here.

from users.models import AllUser

ACCEPTED_EVENT_CATEGORIES = (
		("Education","Education"),
		("Technology","Technology"),
		("Finance","Finance"),
		("Agriculture","Agriculture"),
	)

class Event(models.Model):
    relation = models.ForeignKey(AllUser, help_text="Relation to any system who created this event.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Time event was created")
    updated_at = models.DateTimeField(editable=False,auto_now=True,help_text="Time event was last updated")
    event_title = models.CharField(max_length=100,help_text="Title of the event.")
    event_venue = models.CharField(max_length=50,help_text="Venue of the event.")
    event_description = models.CharField(max_length=300,help_text="Description of the event.")
    event_start_date_time = models.DateTimeField(help_text="Time and Date of event start.")
    event_end_date_time = models.DateTimeField(help_text="Time and Date of event end.")
    event_requires_rsvp = models.BooleanField(default=False,help_text="Indicates whether event requires an RSVP.")
    rsvp_number = models.IntegerField(default=0,help_text="Show the number of people required to RSVP to event.")
    is_showing = models.BooleanField(default=True,help_text="Indicates whether this event is viewable on the website.")
    is_featured = models.BooleanField(default=False,help_text="Shows whether this is a featured event.")
    event_views = models.IntegerField(editable=False,default=0,help_text="Counter for event views.")
    """
    TODO: Event Banner Image
    """

    def __unicode__(self):
        return self.event_title

class EventRSVP(models.Model):
    user_relation = models.ForeignKey(AllUser,help_text="User instance who RSVP'd to event.")
    event_relation = models.ForeignKey(Event,help_text="Event being RSVP'd to.")
    created_at = models.DateTimeField(editable=False,auto_now=True,help_text="Shows when the user RSVP'd.")

    class Meta:
        unique_together = ('user_relation','event_relation')

    def __unicode__(self):
        return '{0} : {1}'.format(self.event_relation.event_title,self.user_relation)

class EventComment(models.Model):
    user_relation = models.ForeignKey(AllUser,help_text="User who is commenting on event.")
    event_relation = models.ForeignKey(Event,help_text="Event being commented on.")
    comment = models.CharField(max_length=300,help_text="User's comment.")
    created_at = models.DateTimeField(editable=False,auto_now=True,help_text="Date & Time comment was made.")

    def __unicode__(self):
        return '{0} : {1}'.format(self.user_relation,self.comment)

class EventReport(models.Model):
    email = models.EmailField(help_text="Email of the reporter")
    details = models.CharField(max_length=150,help_text="Contents of the report.")
    created_at = models.DateTimeField(auto_now=True,help_text="Date & Time that report was made.")

    def __unicode__(self):
        return '{0} : {1}'.format(self.email,self.details)

class EventTag(models.Model):
    relation = models.ForeignKey(Event,help_text="Event being tagged")
    category = models.CharField(max_length=50,choices=ACCEPTED_EVENT_CATEGORIES,help_text="Tag for an event.")

    class Meta:
        unique_together = ('relation','category') #an event can't have two tags which are the exact same

    def __unicode__(self):
        return '{0} : {1}'.format(self.relation.event_title, self.category)
