from rest_framework import (
    serializers,
    exceptions
)

from user.services import (
    AllUserSerializer,
)

from users.models import (
    SparkUser,
    CounsellorUser,
)

from .models import (
    Forum,
    ForumMember,
    ForumMessage,
    ForumRequest,
)

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ('pk','title','description','created_at','updated_at',)

class ForumMemberSerializer(serializers.ModelSerializer):
    forum_relation = ForumSerializer()
    user_relation = AllUserSerializer()
    class Meta:
        model = ForumMember
        fields = ('pk','forum_relation','user_relation',) #won't probably need to use this pk

class ForumRequestSerializer(serializers.ModelSerializer):
    relation = SparkUser()
    class Meta:
        model = ForumRequest
        fields = ('relation','message','created_at',)

class ForumService:
    pass

class ForumMemberService:
    pass

class ForumMessageService:
    pass

class ForumRequestService:
    pass
