import collections

from rest_framework.views import Response
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination

from users.models import AllUser, SparkUser, CounsellorUser

class ChatPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10
    page_size_query_param = 'page_size'

class DRFUtils:
    def check_missing_keys(self,data, required_keys):
        return [key for key in required_keys
            # Key must exist and have a non-empty value.
            if key not in data or
            (isinstance(data[key], str) and len(data[key]) > 0)]

    def keys_not_found(self,missing_keys):
        return Response("Missing POST data keys : %s"  % missing_keys)

class UserUtils:
    """
    when using all auth to authenticate users, rest framework only gets the
    currently logged in user email address. We need to convert this email
    address into a usable user instance.
    """
    def get_user_instance(self,user):
        try:
            user_instance = AllUser.objects.get(email=user)
            return user_instance
        except Exception as e:
            raise exceptions.PermissionDenied(detail="Email provided not found on this server.")

    """
    ->Our problem seems to arise from the fact that when authenticating, we get
    an AllUser instance, which we can't use directly as a SparkUser or
    CounsellorUser instance.
    ->This creates the need for us to have a special function, get_user_instance_updated,
    which return a tuple.
    ->The first object in the tuple is a an updated user instance, and the second object
    is a string which tells us the type of that user instance e.g SparkUser or AllUSer
    """
    def get_user_instance_updated(self,user):
        if user.is_admin == True:
            return (user,'all_user')
        elif user.is_staff == True:
            try:
                counsellor_user = CounsellorUser.objects.get(relation=user)
                return (counsellor_user,'counsellor_user')
            except Exception as e:
                raise exceptions.NotAuthenticated(detail="Unable to verify user details.")
        else:
            try:
                spark_user = SparkUser.objects.get(relation=user)
                return (spark_user,'spark_user')
            except Exception as e:
                raise exceptions.NotAuthenticated(detail="Unable to verify user details.")
"""
class DictUtilities:
    def ordered_dict_to_normal_dict(self,data):
        to_ret = data
        if isinstance(data,collections.OrderDict):
            to_ret = dict(data)

        try:
            for key, value in data.items():
                to_ret[key] = ordered_dict_to_normal_dict(value)
        except AttributeError as e:
            pass

        return to_ret
"""
