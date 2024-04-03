from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.conf import settings
from djangoauthtoken.models import TokenUser, Token
from djangoauthtoken.utils import get_or_create_csrf_token

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    """
    Sign up request
    """
    try:
        data = request.data
        if settings.USERNAME_LOGIN_METHOD:
            username = data['username']
            if 'email' in data.keys():
                email = data['email']
                user, exists = TokenUser.objects.get_or_create(
                    username=username,
                    email=email
                )
            else:
                user, exists = TokenUser.objects.get_or_create(
                    username=username
                )
        else:
            email = data['email']
            if 'username' in data.keys():
                username = data['username']
                user, exists = TokenUser.objects.get_or_create(
                    username=username,
                    email=email
                )
            else:
                user, exists = TokenUser.objects.get_or_create(
                    email=email
                )
        password = data['password']
        user.set_password(password)
        user.save()

        if not exists:
            raise Exception

        user_token = Token(user=user)
        user_token.save()
        _csrf = get_or_create_csrf_token(request)

        return Response({
            "user": user.username if settings.USERNAME_LOGIN_METHOD else user.email,
            "id": user.id,
            "token": user_token.token,
            "refresh_token": user_token.refresh_token,
            "expires_at": user_token.expiry_time
        }, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

