from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)  # changes email to unique and blank to false

    # REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

from django.db import models

# Create your models here.
