from rest_framework import (
    serializers,
    exceptions
)

from .models import (
    AllUser,
    CounsellorUser,
    SparkUser,
    UserAccomplishment,
    UserAccomplishmentTag,
)

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'occupation',
            'phone_number',
            'show_email',
            'show_number',
            'created_at',
            'updated_at',
            )
        partial = True

class CounsellorUserSerializer(serializers.ModelSerializer):
    relation = AllUserSerializer()
    class Meta:
        model = CounsellorUser
        fields = (
        'relation',
        )
        partial = True

class SparkUserSerializer(serializers.ModelSerializer):
    relation = AllUserSerializer()
    class Meta:
        model = SparkUser
        fields = (
        'relation',
        'bio',
        'fb_link',
        'twitter_link',
        )
        partial = True

class UserAccomplishmentSerializer(serializers.ModelSerializer):
    relation = SparkUserSerializer()
    class Meta:
        model = UserAccomplishment
        fields = (
        'spark_user_relation',
        'accomplishment_title',
        'accomplishment_summary',
        'start_date',
        'end_date',
        'created_at',
        'updated_at',
        )
        partial = True

class UserAccomplishmentTagSerializer(serializers.ModelSerializer):
    relation = UserAccomplishmentSerializer()
    class Meta:
        model = UserAccomplishmentTag
        fields = (
        'accomplishment_relation',
        'category',
        )
