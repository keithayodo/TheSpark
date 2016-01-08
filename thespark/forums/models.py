from __future__ import unicode_literals

from django.db import models

# Create your models here.

from users.models import AllUser

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
