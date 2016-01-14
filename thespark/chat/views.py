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

from thespark_drf_utils.drf_utils import (
    DRFUtils,
    UserUtils,
    ChatPagination,
    )

from .services import (
    ConversationService,
    ChatService,
    InboxService,
    )

class AddOrGetConversationView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,id,format=None):#create new conversation or get existing[x]
        conversationService = ConversationService()
        convo = conversationService.get_or_create_conversation(user=request.user,id=id)
        serializer_class = conversationService.get_serializer()
        serialized_data = serializer_class(convo)
        return Response(serialized_data.data)

class ChatView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = ChatPagination
    def get(self,request,id,format=None):#get messages for particular conversation[x]
        chatService = ChatService()
        messages = chatService.get_user_conversation_messages(user=request.user,id=id)
        serializer_class = chatService.get_serializer()
        serialized_data = serializer_class(messages,many=True)
        return Response(serialized_data.data)

    def post(self,request,id,format=None):#post new message to a particular conversation[x]
        required_keys = ["message"]
        dRFUtils = DRFUtils()
        missing_keys = dRFUtils.check_missing_keys(request.data,required_keys)
        if missing_keys:
            raise exceptions.ParseError(detail="Request contained malformed data.")
        else:
            chatService = ChatService()
            new_message = chatService.add_message(sender=request.user,id=id,data=request.data)
            serializer_class = chatService.get_serializer()
            serialized_data = serializer_class(new_message)
            return Response(serialized_data.data)

class LatestConversationMessageView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):#get latest message for every coversation[x]
        inboxService = InboxService()
        latest_convos = inboxService.get_latest_message_per_user_converstation(user=request.user)
        serializer_class = inboxService.get_serializer()
        serialized_data = serializer_class(latest_convos,many=True)
        return Response(serialized_data.data)

class TemplateTestView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/index.html'
    def get(self,request,format=None):#testing django templates + drf[x]
        conversationService = ConversationService()
        convos = conversationService.get_user_conversations(user=request.user)
        serializer_class = conversationService.get_serializer()
        serialized_data = serializer_class(convos,many=True)
        return Response({
            'serializer': serialized_data,
            'convos': convos
        })
