import jwt
from rest_framework import exceptions
from users.models import UserSession, User
from django.utils.translation import gettext as _
from rest_framework_jwt.settings import api_settings
from kwani_api.utils import set_logged_in_user_key
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import (
    get_authorization_header
)
from django.db.models import Q
import re

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        """
        Custom authentication method.
        """
        # Perform custom authentication logic here
        
        # For example, you might want to check a custom header
        token_expired = True
        auth_header = self.get_header(request)
        if auth_header is None:
            return None
        
        try:
            token = self.get_raw_token(auth_header)
            if token is None:
                raise exceptions.AuthenticationFailed('Token expired')
        except AuthenticationFailed:
            return None

        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)
        if user is None:
            raise AuthenticationFailed('Invalid User Session')
        
        user_session = UserSession.objects.filter(user=user,session_token=validated_token).first()
        if user_session:
            token_expired = False
            set_logged_in_user_key(user_session.session_token)
           
        if token_expired:
            raise exceptions.AuthenticationFailed('Signature has expired.')
    
        return (user, token)
    

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if str(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return auth[1]


def bulk_contact_update(recipients):
    for recipient in recipients:
        phone_number = str(recipient['phone_number'])
        name = re.sub(r'\s+', ' ', recipient['name'])
        first_name = name
        last_name = ""

        if name.isspace():
            first_name = name.split('')[0]
            last_name = name.split('')[1]

        if len(phone_number) >= 9:
            contact = User.objects.filter(Q(phone_number__icontains=phone_number[-9:])).first()

            contact.first_name = first_name
            contact.last_name = last_name
            contact.save()
