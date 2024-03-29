from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

from users.models import AllUser, CounsellorUser, SparkUser

class Conversation(models.Model):
    counsellor_instance =  models.ForeignKey(CounsellorUser, help_text="Counsellor instance.")
    user_instance = models.ForeignKey(SparkUser, help_text="Spark user instance.") #May need to change this to AllUser

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

class LastConvoMessage(models.Model):
    relation = models.OneToOneField(Conversation,help_text="Last message sent in this conversation.")
    first_name = models.CharField(max_length=200,help_text="First name of the sender")
    last_name = models.CharField(max_length=200,help_text="Last Name of the sender")
    message = models.CharField(max_length=1000,help_text="Last message sent in this conversation.")
    created_at = models.DateTimeField(help_text="Time when the message was added to the system.")

    def __unicode__(self):
        return '{0} => {1}'.format(self.relation, self.message)

@receiver(post_save,sender=ChatMessage,dispatch_uid="my.post.chat.message.save.signal")
def chat_message_on_save(sender,**kwargs):
    if kwargs.get('created',False):
        new_message = kwargs.get('instance')
        try:
            last_convo = LastConvoMessage.objects.get(relation=new_message.relation)
            last_convo.first_name = new_message.sender.first_name
            last_convo.last_name = new_message.sender.last_name
            last_convo.message = new_message.message
            last_convo.created_at = new_message.created_at
            last_convo.save()
        except LastConvoMessage.DoesNotExist as e:
            new_last_convo = LastConvoMessage.objects.create(
                relation=new_message.relation,
                first_name=new_message.sender.first_name,
                message=new_message.message,
                created_at=new_message.created_at)
            new_last_convo.save()
