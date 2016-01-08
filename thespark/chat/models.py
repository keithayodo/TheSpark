from __future__ import unicode_literals

from django.db import models

# Create your models here.

from users.models import AllUser, CounsellorUser, SparkUser

class Conversation(models.Model):
    counsellor_instance =  models.ForeignKey(CounsellorUser, help_text="Counsellor instance.")
    user_instance = models.ForeignKey(SparkUser, help_text="Spark user instance.")

    class Meta:
        unique_together = ('counsellor_instance','user_instance')

    def __unicode__(self):
        return '{0} : {1}'.format(self.counsellor_instance.relation,self.user_instance.relation)

class ChatMessage(models.Model):
    relation = models.ForeignKey(Conversation,help_text="Conversation that the message belongs to.")
    sender = models.ForeignKey(AllUser,help_text="Sender of the message.")
    message = models.CharField(max_length=1000,help_text="Message contents.")
    created_at = models.DateTimeField(editable=False,auto_now_add=True,help_text="Time when message was created.")

    def __unicode__(self):
        return '{0} :{1}'.format(self.sender,self.message)
