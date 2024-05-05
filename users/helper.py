import jwt
from rest_framework import exceptions
from django.utils.encoding import smart_text
from users.models import UserSession
from django.utils.translation import ugettext as _
from rest_framework_jwt.settings import api_settings
from kwani_api.utils import set_logged_in_user_key
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """
    def authenticate(self, request):
        
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None
        try:
            token_expired = True
            payload = jwt_decode_handler(jwt_value)
            if payload['user_id'] is None:
                raise exceptions.AuthenticationFailed('Token expired')
            user_sessions = UserSession.objects.filter(user__id=payload['user_id'])
            if user_sessions:
                for user_session in user_sessions:
                    if user_session.session_token:
                        if user_session.session_token in str(jwt_value):
                            token_expired = False
                            set_logged_in_user_key(user_session.session_token)
            if token_expired:
                raise exceptions.AuthenticationFailed('Signature has expired.')
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return (user, payload)
    
    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()
        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return auth[1]
        
        