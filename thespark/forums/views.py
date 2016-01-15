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

from thespark_drf_utils.drf_utils import DRFUtils

from .services import (
    MemberService,
    ForumMessageService,
    ForumRequestService,
    LastForumMessageService,
    #ForumReport,
    ForumReportService,
    ForumService,
)

class ForumsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):
        forumService = ForumService()
        forums = forumService.get_all_forums()
        serializer_class = forumService.get_serializer()
        serialized_data = serializer_class(forums,many=True)
        return Response(serialized_data.data)

class ForumView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id,format=None):#get all messages for a particulat forum
        forumMessageService = ForumMessageService()
        messages = forumMessageService.get_forum_messages(user=request.user,id=id)
        serializer_class = forumMessageService.get_serializer()
        serialized_data = serializer_class(messages,many=True)
        return Response(serialized_data.data)

    def post(self,request,id,format=None):#post a message to a particular forum
        required_keys = ["message"]
        dRFUtils = DRFUtils()
        missing_keys = dRFUtils.check_missing_keys(request.data,required_keys)
        if missing_keys:
            raise exceptions.ParseError(detail="Request contained missing required keys.")
        else:
            forumMessageService = ForumMessageService()
            new_message = forumMessageService.add_new_message(user=request.user,id=id,data=request.data)
            serializer_class = forumMessageService.get_serializer()
            serialized_data = serializer_class(new_message)
            return Response(serialized_data.data)

class LastForumMessageView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,format=None):#get latest message for all forums a user is subscribed to
        last_forum_message_service = LastForumMessageService()
        messages = last_forum_message_service.get_latest_message_per_forum_for_user(user=request.user)
        serializer_class = last_forum_message_service.get_serializer()
        serialized_data = serializer_class(messages,many=True)
        return Response(serialized_data.data)

class SubscribeForumView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,id,format=None):#allow a spark user to subscribe to a forum
        member_service = MemberService()
        subscriber = member_service.subscribe_user_to_forum(user=request.user,id=id)
        serializer_class = member_service.get_serializer()
        serialized_data = serializer_class(subscriber)
        return Response(serialized_data.data)

class UnsubscribeForumView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,id,format=None):#Allow a spark user to unsubscribe from a forum
        member_service = MemberService()
        is_deleted = member_service.unsubscribe_user_from_forum(user=request.user,id=id)
        deleted = {'deleted':is_deleted}
        return Response(deleted)

class ForumRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,format=None):#Allow a spark user to request for a new forum
        required_keys = ["forum_name","message"]
        dRFUtils = DRFUtils()
        missing_keys = dRFUtils.check_missing_keys(request.data,required_keys)
        if missing_keys:
            raise exceptions.ParseError(detail="Request contained missing required keys.")
        else:
            forumRequestService = ForumRequestService()
            forum_request = forumRequestService.add_new_forum_request(user=request.user,data=request.data)
            serializer_class = forumRequestService.get_serializer()
            serialized_data = serializer_class(forum_request)
            return Response(serialized_data.data)

class ForumReportView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,id,format=None):
        required_keys = ["message"]
        dRFUtils = DRFUtils()
        missing_keys = dRFUtils.check_missing_keys(request.data,required_keys)
        if missing_keys:
            raise exceptions.ParseError(detail="Request contained missing required keys.")
        else:
            forumReportService = ForumReportService()
            print 'No missing keys were found :)'
            forum_report = forumReportService.add_new_forum_report(user=request.user,data=request.data,id=id)
            serializer_class = forumReportService.get_serializer()
            serialized_data = serializer_class(forum_report)
            return Response(serialized_data.data)
