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
            'pk',
            #'email',
            'first_name',
            'last_name',
            'occupation',
            #'phone_number',
            'show_email',
            'show_number',
            #'created_at',
            #'updated_at',
        )

class CounsellorUserSerializer(serializers.ModelSerializer):
    relation = AllUserSerializer()
    class Meta:
        model = CounsellorUser
        fields = (
        'relation',
        )

class SparkUserSerializer(serializers.ModelSerializer):

    def __init__(self,*args,**kwargs):
        #Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields',None)

        #Instantiate superclass normally
        super(SparkUserSerializer,self).__init__(*args,**kwargs)

        """
        if fields is None:
            show_email = self.fields.get('show_email',default=False)
            if show_email == False:
                self.fields.pop('email')
        """
        """
        if fields is not None:
            #Remove any fields specified in the fields argument of the serializer
            removed = set(fields)
            existing = set(self.fields.keys())
            for field_name in removed:
                self.fields.pop(field_name)
        """
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
