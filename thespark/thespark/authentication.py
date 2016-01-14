from users.models import AllUser
from rest_framework import authentication
from rest_framework import exceptions

"""
This is a helper clas to get our custom user model
to work with DRF
"""
class ApiAuthentication(authentication.BaseAuthentication):
    def authenticate(self,request):
        username = request.META.get('X_EMAIL')
        if not username:
            return None
        try:
            user = AllUser.objects.get(email=username)
        except AllUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
            return (user,None)
