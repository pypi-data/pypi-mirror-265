from django.contrib.auth.models import AbstractUser
import pytz
import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

from djangoauthtoken.models import Base
from djangoauthtoken.models.custom_fields import CaseInsensitiveEmailField


tz = [(item, datetime.datetime.now(pytz.timezone(item)).strftime("%z") + " " + item) for item in pytz.all_timezones]

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}',
    message="Phone numbers must be in International format: '+14169058762'. Up to 15 digits "
)


class TokenUser(AbstractUser, Base):

    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True)
    if not settings.USERNAME_LOGIN_METHOD:
        email = CaseInsensitiveEmailField(max_length=Base.MAX_LENGTH_LARGE, unique=True)
        username = CaseInsensitiveEmailField(max_length=Base.MAX_LENGTH_LARGE, blank=True, required=False)
        REQUIRED_FIELDS = ["email"]
    
    def __str__(self) -> str:
        return self.username if settings.USERNAME_LOGIN_METHOD else self.email
