from rest_framework import (
    serializers,
    exceptions
)

from thespark_drf_utils.drf_utils import DRFUtils

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
        fields = ('counsellor_instance','user_instance')

class ChatMessageSerializer(serializers.ModelSerializer):
    relation = ConversationSerializer()
    class Meta:
        model = ChatMessage
        fields = ('relation','message','created_at')
        partial = True
    """
    def create(self,validated_data):
        conversation_data = validated_data.pop('relation')
        chat_message = User.objects.create(**validated_data)
    """

class LastConvoMessageSerializer(serializers.ModelSerializer):
    relation = ConversationSerializer()
    class Meta:
        model = LastConvoMessage
        fields = ('first_name','message','created_at')

class ConversationService:

    def __init__(self):
        self.viewset = Conversation.objects.all()

    def get_serializer(self):
        return ConversationSerializer
    """
    def get_counsellor(self,id):
        try:
            counsellor = CounsellorUser.objects.get(pk=id)
            return counsellor
        except Exception as e:
            raise exceptions.NotFound(detail="Counsellor with provide id not found.")

    def get_spark_user(self,id):
        try:
            spark_user = SparkUser.objects.get(pk=id)
            return spark_user
        except Exception as e:
            raise exceptions.NotFound(detail="Spark user with provided id not found.")
    """
    def create_new_conversation_by_spark_user(self,spark_user,counsellor_id):
        try:
            convo = Conversation.objects.get(counsellor_instance__pk=counsellor_id,user_instance=user)
            return convo
        except Conversation.DoesNotExist as e:
            new_convo = Conversation.objects.create(counsellor_instance__pk=counsellor_id,user_instance=user_instance)
            new_convo.save()
            return new_convo


    def create_new_conversation_by_consellor(self,counsellor,spark_user_id):
        try:
            convo = Conversation.objects.get(user_instance__pk=spark_user_id,counsellor_instance=counsellor)
            return convo
        except Conversation.DoesNotExist as e:
            new_convo = Conversation.objects.create(user_instance__pk=spark_user_id,counsellor_instance=counsellor)
            new_convo.save()
            return new_convo

    def get_or_create_conversation(self,user,id):
        if isinstance(user,SparkUser):
            convo = self.create_new_conversation_by_spark_user(spark_user=user,counsellor_id=id)
            return convo
        elif isinstance(user,CounsellorUser):
            convo = self.create_new_conversation_by_consellor()
            return convo
        else:
            raise exceptions.PermissionDenied(detail="You don't have access to this resource via API")

    def does_user_belong_to_convo(self,user,id):
        try:
            if isinstance(user,SparkUser):
                convo = self.viewset.get(user_instance=user,pk=id)
                return convo
            elif isinstance(user,CounsellorUser):
                convo = self.viewset.get(counsellor_instance=user,pk=id)
                return convo
            else:
                raise exceptions.PermissionDenied(detail="Yo do not have permission to view this resource via API.")
        except Conversation.DoesNotExist as e:
            raise exceptions.NotFound(detail="Conversation with provided id not found.")

    def get_user_conversations(self,user):
        if isinstance(user,SparkUser):
            convos = self.viewset.filter(user_instance=user)
            return convos
        elif isinstance(user,CounsellorUser):
            convos = self.viewset.filter(counsellor_instance=user)
            return convos
        else:
            raise exceptions.PermissionDenied(detail="No permission to view this content via API.")


class ChatService:

    def __init__(self):
        self.viewset = ChatMessage.objects.all()

    def get_serializer(self):
        ChatMessageSerializer

        #method placed here because return value can be serialized with this class's serializer
    def get_user_conversation_messages(self,user,id):
        conversationService = ConversationService()
        convo = conversationService.does_user_belong_to_convo(user=user,id=id)
        messages = ChatMessage.objects.filter(relation=convo)
        return messages

    #id id ID of convo we're adding the message to
    def add_message(self,sender,id,data):
        conversationService = ConversationService()
        convo = conversationService.does_user_belong_to_convo(user=sender,id=id)
        serializer_class = self.get_serializer()
        data['relation'] = convo
        serialized_data = serializer_class(data=data)
        if serialized_data.is_valid():
            new_message = ChatMessage.create(relation=convo,sender=sender,message=message)
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
        if isinstance(user,SparkUser):
            latest_messages = LastConvoMessage.objects.get(relation__user_instance=user).order_by('created_at')
            return latest_messages
        elif isinstance(user,CounsellorUser):
            latest_messages = LastConvoMessage.objects.get(relation__counsellor_instance=user).order_by('created_at')
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
