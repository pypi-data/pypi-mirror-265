import jwt

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from djangoauthtoken.models import TokenUser, Token


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def refresh_token(request):
    """
    Refresh Token request.
    """
    try:
        data = request.data
        refresh_token = data['refresh_token']
        refresh_token_decode = jwt.decode(refresh_token,
                                          settings.JWT_SECRET,
                                          algorithms=settings.JWT_ALGO)
        # Check for user.
        user = TokenUser.objects.get(id=refresh_token_decode['user_id'])
        # check for token.
        token_user = Token.objects.get(user=user, refresh_token=refresh_token)
        if not token_user:
            raise ObjectDoesNotExist
        # save new token.
        token = Token(user=user)
        token.save()

        return Response({
            "id": user.id,
            "user": token_user.username if settings.USERNAME_LOGIN_METHOD else token_user.email,
            "token": token.token,
            "refresh_token": token.refresh_token,
            "expires_at": token.expiry_time
        },
            status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
