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

from .models import (
    Conversation,
    ChatMessage,
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

class ConversationService:

    def __init__(self):
        self.viewset = Conversation.objects.all()

    def get_post_data(self,user,data):
        return None

    def get_serializer(self):
        return ConversationSerializer

    def create_new_conversation_by_user(self,counsellor,user):
        try:
            new_convo = Conversation.objects.create(counsellor_instance=counsellor,user_instance=user_instance)
            new_convo.save()
            return new_convo
        except Conversation.IntegrityError as e:
            raise
    """
    def create_new_conversation_by_consellor(self,counsellor,user):
        return None
    """

    #check conversation using its id, user
    def check_conversation_exist(self,user,id):
        #Use this to very if user belongs to conversation
        try:
            conversation = Conversation.objects.get(pk=id)
            return conversation
        except Exception as e:
            raise exceptions.NotFound(detail="Conversation does not exist.")

    def get_user_conversations(self,user):
        if isinstance(user,SparkUser):
            convos = self.viewset.filter(user_instance=user)
        if isinstance(user,CounsellorUser):
            convos = self.viewset.filter(counsellor_instance=user)
        return convos

    def get_user_conversation(self,user,id):
        try:
            if isinstance(user,SparkUser):
                convo = self.viewset.get(user_instance=user,pk=id)
            if isinstance(user,CounsellorUser):
                convo = self.viewset.get(counsellor_instance=user,pk=id)
        except Conversation.NotFound as e:
            raise exceptions.NotFound(detail="Conversation does not exist.")

        return convo

    """
    def get_user_conversations_counsellor_user(self,user):
        convos = self.viewset.filter(counsellor_instance=user)
        return convos
    """

class ChatService:

    def __init__(self):
        self.viewset = ChatMessage.objects.all()

    def get_post_data(self,user,data):
        return None

    #add new message to chat table
    """
    relation: Conversation ID of the message
    """
    def add_message(self,sender,message,relation):
        new_message = ChatMessage.create(relation=relation,sender=sender,message=message)
        update_last_convo_message(new_message=new_message)
        return new_message

    def get_messages_for_conversation(self,user,conversation):
        #TODO: Check whether user belongs to this conversation. Do this in ConversationService.
        messages = self.viewset.filter(relation=conversation)

    def update_last_convo_message(self,new_message):
        last_message = LastConvoMessage.objects.create(relation=new_message.relation,full_name=new_message.sender.get_short_name(),message=new_message.message,created_at=new_message.created_at)
        last_message.save()
        return last_message

class InboxService:
    #pass convo id to get last message
    def get_latest_message_per_converstation(self,user):
        latest_messages = LastConvoMessage.objects.filter(sender=user).order_by('created_at')
        return latest_messages



    """
    def get_latest_message_per_converstation(self,user):
        conversations = ConversationService().get_user_conversations(user=user)
        last_message_per_convo = conversations.map(lambda convo: ChatMessage.objects.filter(relation=convo).order_by('created_at')[:1],conversations)
        return last_message_per_convo
    """
