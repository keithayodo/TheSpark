from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView, Response, status
from rest_framework.permissions import (
IsAuthenticated,
AllowAny,
IsAdminUser,
IsAuthenticatedOrReadOnly,
)
from rest_framework import exceptions

from .services import ConversationService, ChatService

class ConversationView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id,format=None):
        conversationService = ConversationService()
        convo = conversationService.check_conversation_exist(user=request.user,id=id)
        #line above probabbly won't be here in production
        serializer_class = conversationService.get_serializer()
        serialized_data = serializer_class(convo)
        return Response(serialized_data.data)
