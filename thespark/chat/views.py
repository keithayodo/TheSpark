from django.shortcuts import render

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

from .services import (
    ConversationService,
    ChatService,
    InboxService,
    )

class ConversationView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id,format=None):
        conversationService = ConversationService()
        convo = conversationService.check_conversation_exist(user=request.user,id=id)
        #line above probabbly won't be here in production (should be in services.py)
        serializer_class = conversationService.get_serializer()
        serialized_data = serializer_class(convo)
        return Response(serialized_data.data)

class LatestConversationMessageView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        inboxService = InboxService()
        latest_convos = inboxService.get_latest_message_per_user_converstation(user=request.user)
        serializer_class = inboxService.get_serializer()
        serialized_data = serializer_class(latest_convos,many=True)
        return Response(serialized_data.data)

#drf template test
class TemplateTestView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/index.html'
    def get(self,request,format=None):
        conversationService = ConversationService()
        convos = conversationService.get_user_conversations(user=request.user)
        serializer_class = conversationService.get_serializer()
        serialized_data = serializer_class(convos,many=True)
        return Response({
            'serializer': serialized_data,
            'convos': convos
        })
