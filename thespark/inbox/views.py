from django.shortcuts import render

from itertools import chain
import json

# Create your views here.

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import (
IsAuthenticated,
AllowAny,
IsAdminUser,
IsAuthenticatedOrReadOnly,
)
from rest_framework import exceptions

from chat.services import InboxService
from forums.services import LastForumMessageService

from chat.models import LastConvoMessage
from forums.models import LastForumMessage

class GetInbox(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        inboxService = InboxService()
        lastForumMessageService = LastForumMessageService()
        chat_inbox = inboxService.get_latest_message_per_user_converstation(user=request.user)
        forum_inbox = lastForumMessageService.get_latest_message_per_forum_for_user(user=request.user)
        combined_inbox = sorted(chain(chat_inbox,forum_inbox),
                            key=lambda instance: instance.created_at,reverse=True)
        inbox = []
        print 'created empty list'
        for message in combined_inbox:
            my_dict = {}
            if isinstance(message,LastConvoMessage):
                print 'chat message'
                my_dict['id'] = message.relation.pk
                my_dict['message_type'] = 'chat'
                my_dict['first_name'] = message.first_name
                my_dict['last_name'] = message.last_name
                my_dict['created_at'] = message.created_at
                my_dict['message'] = message.message
                inbox.append(my_dict)
            elif isinstance(message,LastForumMessage):
                my_dict['id'] =  message.relation.pk
                my_dict['message_type'] = 'forum'
                my_dict['first_name'] = message.first_name
                my_dict['last_name'] = message.last_name
                my_dict['created_at'] = message.created_at
                my_dict['message'] = message.message
                inbox.append(my_dict)
            else:
                print message.__class__.__name__ #log statement here
            print message

        return Response(inbox)
