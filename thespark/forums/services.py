from rest_framework import (
    serializers,
    exceptions
)

from thespark_drf_utils.drf_utils import UserUtils

from users.services import (
    AllUserSerializer,
    SparkUserSerializer,
)

from users.models import (
    SparkUser,
    CounsellorUser,
)

from .models import (
    Forum,
    Member,
    ForumMessage,
    ForumRequest,
    LastForumMessage,
    ForumReport,
)

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ('pk','title','description','created_at','updated_at',)

class MemberSerializer(serializers.ModelSerializer):
    forum_relation = ForumSerializer()
    user_relation = AllUserSerializer()
    class Meta:
        model = Member
        fields = ('pk','forum_relation','user_relation',) #won't probably need to use this pk

class ForumMessageSerializer(serializers.ModelSerializer):
    sender = AllUserSerializer(required=False)
    relation = ForumSerializer(required=False)
    class Meta:
        model = ForumMessage
        fields = ('sender','relation','created_at','message',)#in production, we could probably do away with 'relation' field

class ForumRequestSerializer(serializers.ModelSerializer):
    relation = SparkUserSerializer(required=False)
    class Meta:
        model = ForumRequest
        fields = ('relation','forum_name','message','created_at',)

class LastForumMessageSerializer(serializers.ModelSerializer):
    relation = ForumSerializer()
    class Meta:
        model = LastForumMessage
        fields = ('relation','first_name','last_name','message','created_at')

class ForumReportSerializer(serializers.ModelSerializer):
    relation = SparkUserSerializer(required=False)
    forum_relation = ForumSerializer()
    class Meta:
        model = ForumReport
        fields = ('relation','forum_relation','message','created_at')


"""
1 => Get the latest mesasge in all forums a user is subscribed to[GET][x][x][x]
2 => Subcribe a user to a forum[POST][x][x][x]
3 => Unsubscribe a user from a forum[POST][x][x][x]
4 => Get a list of forum messages[GET][x][x][x]
5 => Allow a spark user to request a forum[POST][x][x][x]
6 => Allow a spark user to report a forum[POST][x][x][x]
7 => Allow a spark user to post a message to a forum[POST][x][x][x]
8 => Get a list of available Forums[GET][x][x][x]
"""

class ForumService:
    def __init__(self):
        self.viewset = Forum.objects.all()

    def get_serializer(self):
        return ForumSerializer

    def does_forum_exist(self,id):
        try:
            forum = Forum.objects.get(pk=id)
            return forum
        except Exception as e:
            return None

    def get_all_forums(self):
        forums = self.viewset
        return forums

class MemberService:
    def __init__(self):
        self.viewset = Member.objects.all()

    def get_serializer(self):
        return MemberSerializer

    def is_user_subscribed_to_forum(self,user,id):
        try:
            forum_member = Member.objects.get(user_relation=user,forum_relation__id=id)
            return forum_member
        except Member.DoesNotExist as e:
            return None

    #assumes user is authenticated
    #return None if user is already subscribed
    def subscribe_user_to_forum(self,user,id):
        forum_member = self.is_user_subscribed_to_forum(user=user,id=id)
        if forum_member is not None:
            return forum_member
        else:
            try:
                forum = Forum.objects.get(pk=id)
                new_subscriber = Member.objects.create(forum_relation=forum,user_relation=user)
                return new_subscriber
            except Forum.DoesNotExist as e:
                raise exceptions.NotFound(detial="The forum id provided was not found on this server.")


    #returns None if unable to verify user subscription
    def unsubscribe_user_from_forum(self,user,id):
        forum_member = self.is_user_subscribed_to_forum(user=user,id=id)
        if forum_member is not None:
            forum_member.delete()
            return True #return true on delete, return object on create
        else:
            raise exceptions.NotFound(detail="It seems that you are not a member of this forum.")

class ForumMessageService:
    def __init__(self):
        self.viewset = ForumMessage.objects.all()

    def get_serializer(self):
        return ForumMessageSerializer

    def add_new_message(self,user,id,data):
        memberService = MemberService()
        member = memberService.is_user_subscribed_to_forum(user=user,id=id)
        if member is not None:
            serializer_class = self.get_serializer()
            serialized_data = serializer_class(data=data)
            if serialized_data.is_valid():
                new_forum_message = ForumMessage.objects.create(
                    sender = user,
                    relation = member.forum_relation,
                    message = data['message']
                )
                #new_forum_message.save()
                return new_forum_message
            else:
                raise exceptions.ParseError(detail=serialized_data.errors)
        else:
            raise exceptions.NotFound(detail="User is not subscrided to forum, or forum does not exist.")

    def get_forum_messages(self,user,id):
        memberService = MemberService()
        forum_member = memberService.is_user_subscribed_to_forum(user=user,id=id)
        if forum_member is not None:
            messages = ForumMessage.objects.filter(relation=forum_member.forum_relation).order_by('-created_at')
            return messages
        else:
            raise exceptions.NotFound(detail="User is not subscrided to forum, or forum does not exist.")

class ForumRequestService:
    def __init__(self):
        self.viewset = ForumRequest.objects.all()

    def get_serializer(self):
        return ForumRequestSerializer

    def add_new_forum_request(self,user,data):
        userUtils = UserUtils()
        user_type = userUtils.get_user_instance_updated(user=user)
        if user_type[1] == 'spark_user':
            forumService = ForumService()
            serializer_class = self.get_serializer()
            serialized_data = serializer_class(data=data)
            if serialized_data.is_valid():
                new_forum_request = ForumRequest.objects.create(
                    relation = user_type[0],
                    forum_name = data['forum_name'],
                    message = data['message']
                    )
                #new_forum_request.save()
                return new_forum_request
            else:
                raise exceptions.ParseError(detail=serialized_data.data)
        else:
            raise exceptions.PermissionDenied(detail="You cannot view this resource via API.")

class LastForumMessageService:
    def __init__(self):
        self.viewset = LastForumMessage.objects.all()

    def get_serializer(self):
        return LastForumMessageSerializer

    def get_latest_message_per_forum_for_user(self,user):
        """
        print 'we got to get_latest_message_per_forum_for_user function :)'
        matched_forums = Forum.objects.filter(member__user_relation=user)
        print 'we matched_forums :)'
        latest_messages = LastForumMessage.objects.filter(forum__in=macthed_forums).order_by('-created_at')
        """
        latest_messages = LastForumMessage.objects.filter(relation__member__user_relation=user).order_by('-created_at')
        """
        Query above explained:
        ->First of find all latest messages which match a relation objects
        ->Now that we have 'access' to that relation object, use a reverse relationship to find the member model, specified in underscore
        """
        return latest_messages

class ForumReportService:
    def __init__(self):
        self.viewset = ForumReport.objects.all()

    def get_serializer(self):
        return ForumReportSerializer

    def add_new_forum_report(self,user,data,id):
        print 'We got to add_new_forum_report'
        forumService = ForumService()
        forum = forumService.does_forum_exist(id=id)
        if forum is not None:
            userUtils = UserUtils()
            user_type = userUtils.get_user_instance_updated(user=user)
            if user_type[1] == 'spark_user':
                new_forum_report = ForumReport.objects.create(
                    relation = user_type[0],
                    forum_relation = forum,
                    message = data['message']
                )
                #new_forum_report.save()
                return new_forum_report
            else:
                raise exceptions.PermissionDenied(detail="You do not have permission to your request via API.")
        else:
            raise exceptions.NotFound(detail="Forum id supplied was not found.")
