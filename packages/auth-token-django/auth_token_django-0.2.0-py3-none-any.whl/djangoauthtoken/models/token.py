import jwt

from django.db import models
from django.conf import settings

from djangoauthtoken.models import Base, TokenUser
from djangoauthtoken.utils import get_epoch


class Token(Base):
    token = models.CharField(max_length=Base.MAX_LENGTH_LARGE)
    refresh_token = models.CharField(max_length=Base.MAX_LENGTH_LARGE)
    expiry_time = models.IntegerField(default=settings.EXPIRY)
    user = models.ForeignKey(TokenUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        epoch_time = get_epoch()
        # Create a common function for this.
        self.token = jwt.encode({
            "user_id": self.user.id,
            "user": self.user.username if settings.USERNAME_LOGIN_METHOD else self.user.email,
            "type": settings.AUTH_TOKEN,
            "date": epoch_time
        },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGO
        )

        self.refresh_token = jwt.encode({
            "user_id": self.user.id,
            "user": self.user.username if settings.USERNAME_LOGIN_METHOD else self.user.email,
            "type": settings.REFRESH_TOKEN,
            "date": epoch_time
        },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGO
        )
        super(Token, self).save(*args, **kwargs)
