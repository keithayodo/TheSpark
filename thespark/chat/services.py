import logging

from rest_framework import (
    serializers,
    exceptions
)

from thespark_drf_utils.drf_utils import UserUtils

from users.services import (
    AllUserSerializer,
    CounsellorUserSerializer,
    SparkUserSerializer,
)

from users.models import (
    SparkUser,
    CounsellorUser,
)

from .models import (
    Conversation,
    ChatMessage,
    LastConvoMessage,
)


class ConversationSerializer(serializers.ModelSerializer):
    counsellor_instance = CounsellorUserSerializer()
    user_instance = SparkUserSerializer()
    class Meta:
        model = Conversation
        fields = ('pk','counsellor_instance','user_instance')

class ChatMessageSerializer(serializers.ModelSerializer):
    relation = ConversationSerializer(required=False)
    class Meta:
        model = ChatMessage
        fields = ('pk','relation','message','created_at')

class LastConvoMessageSerializer(serializers.ModelSerializer):
    relation = ConversationSerializer()
    class Meta:
        model = LastConvoMessage
        fields = ('relation','first_name','last_name','message','created_at')

class ConversationService:

    def __init__(self):
        self.viewset = Conversation.objects.all()

    def get_serializer(self):
        return ConversationSerializer

    def get_counsellor(self,id):
        try:
            counsellor = CounsellorUser.objects.get(relation_id=id)#lookup reverse relationship
            return counsellor
        except CounsellorUser.DoesNotExist as e:
            raise exceptions.NotFound(detail="The counsellor with provided id was not found.")

    def get_spark_user(self,id):
        try:
            spark_user = SparkUser.objects.get(relation_id=id)
            return spark_user
        except SparkUser.DoesNotExist as e:
            raise exceptions.NotFound(detail="The spark user with provided id was not found.")

    def create_new_conversation_by_spark_user(self,spark_user,counsellor_id):
        try:
            counsellor_instance = self.get_counsellor(id=counsellor_id)
            convo = Conversation.objects.get(counsellor_instance=counsellor_instance,user_instance=spark_user)
            return convo
        except Conversation.DoesNotExist as e:
            new_convo = Conversation.objects.create(counsellor_instance=counsellor_instance,user_instance=spark_user)
            #new_convo.save()
            return new_convo


    def create_new_conversation_by_consellor(self,counsellor,spark_user_id):
        try:
            spark_user = self.get_spark_user(id=spark_user_id)
            print 'we got a spark user :)'
            convo = Conversation.objects.get(user_instance=spark_user,counsellor_instance=counsellor)
            return convo
        except Conversation.DoesNotExist as e:
            new_convo = Conversation.objects.create(user_instance=spark_user,counsellor_instance=counsellor)
            #new_convo.save()
            return new_convo

    def get_or_create_conversation(self,user,id):
        userUtils = UserUtils()
        user_type = userUtils.get_user_instance_updated(user=user)
        if user_type[1] == 'spark_user':
            convo = self.create_new_conversation_by_spark_user(spark_user=user_type[0],counsellor_id=id)
            return convo
        elif user_type[1] == 'counsellor_user':
            print 'request is from counsellor :)'
            convo = self.create_new_conversation_by_consellor(counsellor=user_type[0],spark_user_id=id)
            return convo
        else:
            raise exceptions.PermissionDenied(detail="You don't have access to this resource via API")

    def does_user_belong_to_convo(self,user,id):
        try:
            userUtils = UserUtils()
            user_type = userUtils.get_user_instance_updated(user=user)
            if user_type[1] == 'spark_user':
                convo = self.viewset.get(user_instance=user_type[0],pk=id)
                return convo
            elif user_type[1] == 'counsellor_user':
                convo = self.viewset.get(counsellor_instance=user_type[0],pk=id)
                return convo
            else:
                raise exceptions.PermissionDenied(detail="Yo do not have permission to view this resource via API.")
        except Conversation.DoesNotExist as e:
            raise exceptions.NotFound(detail="Conversation with provided id not found.")

class ChatService:

    def __init__(self):
        self.viewset = ChatMessage.objects.all()

    def get_serializer(self):
        return ChatMessageSerializer

        #method placed here because return value can be serialized with this class's serializer
    def get_user_conversation_messages(self,user,id):
        conversationService = ConversationService()
        convo = conversationService.does_user_belong_to_convo(user=user,id=id)
        print 'user belongs to convo'
        messages = ChatMessage.objects.filter(relation=convo).order_by('-created_at')
        return messages

    #id id ID of convo we're adding the message to
    def add_message(self,sender,id,data):
        try:
            data = data.dict()
        except AttributeError as e:
            data = data
        print data
        conversationService = ConversationService()
        convo = conversationService.does_user_belong_to_convo(user=sender,id=id)
        serializer_class = self.get_serializer()
        print 'we serialized the data :)'
        #print data['relation']
        serialized_data = serializer_class(data=data)
        if serialized_data.is_valid():
            print serialized_data
            print 'we validated the data :)'
            new_message = ChatMessage.objects.create(relation=convo,sender=sender,message=data['message'])
            #new_message.save()
            return new_message
        else:
            raise exceptions.ParseError(detail=serialized_data.errors)

    """
    #we use database signals to do this now
    def update_last_convo_message(self,new_message):
        last_message = LastConvoMessage.objects.create(relation=new_message.relation,full_name=new_message.sender.get_short_name(),message=new_message.message,created_at=new_message.created_at)
        last_message.save()
        return last_message
    """

class InboxService:
    #pass convo id to get last message

    def get_serializer(self):
        return LastConvoMessageSerializer

    def get_latest_message_per_user_converstation(self,user):
        userUtils = UserUtils()
        #print user.__class__.__name__ #method to show class name of object instance
        #print "We got here"
        user_type = userUtils.get_user_instance_updated(user=user)
        if user_type[1] is 'spark_user':
            latest_messages = LastConvoMessage.objects.filter(relation__user_instance=user_type[0]).order_by('-created_at')#order from earliest to latest
            return latest_messages
        elif user_type[1] is 'counsellor_user':
            latest_messages = LastConvoMessage.objects.filter(relation__counsellor_instance=user_type[0]).order_by('-created_at')
            return latest_messages
        else:
            raise exceptions.PermissionDenied(detail="You don't have the required permission to view this resource via API.")

    """
    #Original 'push method of getting the latest messages for a coversation'
    def get_latest_message_per_converstation(self,user):
        conversations = ConversationService().get_user_conversations(user=user)
        last_message_per_convo = conversations.map(lambda convo: ChatMessage.objects.filter(relation=convo).order_by('created_at')[:1],conversations)
        return last_message_per_convo
    """
