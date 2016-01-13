from __future__ import unicode_literals

from django.db import models

# Create your models here.

from users.models import AllUser, SparkUser

class Forum(models.Model):
    title = models.CharField(max_length=50,help_text="Title of the forum.")
    description = models.CharField(max_length=150,help_text="Description of the forum.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="The Date & Time when this forum was created.")
    updated_at = models.DateTimeField(editable=False,auto_now=True,help_text="Last time forum details were updated.")

    def __unicode__(self):
        return self.title

class ForumMember(models.Model):
    forum_relation = models.ForeignKey(Forum,help_text="Forum which user is a memebr.")
    user_relation = models.ForeignKey(AllUser, help_text="User who has joined a forum.")

    class Meta:
        unique_together = ('forum_relation','user_relation')

    def __unicode__(self):
        return '{0} : {1}'.format(self.user_relation,self.forum_relation.title)

    """
    TODO: Decide whether to denormalize this field, by adding both first & last name of user.
    """

class ForumMessage(models.Model):
    sender = models.ForeignKey(AllUser,help_text="Sender of the message")
    relation = models.ForeignKey(Forum,help_text="Forum that message belongs to.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Date of Time of message posting.")
    message = models.CharField(max_length=1000,help_text="Mesasge content.")

    def __unicode__(self):
        return '{0} :{1}'.format(self.sender,self.message)

class LastForumMessage(models.Model):
    relation = models.OneToOneField(Forum,help_text="Last/latest message sent in forum.")
    first_name = models.CharField(max_length=200,help_text="First name of last message sender.")
    last_name = models.CharField(max_length=200,help_text="Last name of last message sender.")
    mesasge = models.CharField(max_length=1000,help_text="Last message sent in forum.")
    created_at = models.DateTimeField(help_text="Time when last message was sent in forum.")

    def __unicode__(self):
        return '{0} :{1}'.format(self.relation,self.message)

class ForumRequest(models.Model):
    relation = models.ForeignKey(SparkUser,help_text="Spark user requesting a new forum.")
    forum_name = models.CharField(max_length=50,help_text="Proposed forum name.")
    message = models.CharField(max_length=1000,help_text="Message content.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Date and time of forum request submission.")

    def __unicode__(self):
        return '{0} : {1}'.format(self.relation,self.forum_name)

class ForumReport(models.Model):
    relation = models.ForeignKey(SparkUser,help_text="Spark user who is reporting a forum.")
    forum_relation = models.ForeignKey(Forum,help_text="Forum being reported.")
    message = models.CharField(max_length=1000,help_text="Message of reporter.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Date and time when the forum was reported.")

    def __unicode__(self):
        return '{0} => {1}'.format(self.relation, self.forum_relation.title)
