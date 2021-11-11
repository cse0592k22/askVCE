from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from askvce.settings import EMAIL_FORMAT
import re


class UserManager(BaseUserManager):
    """
    Custom Manager for custom model to create user and superuser
    """

    def create_user(self, email, user_name, first_name, last_name, dob, grad_year, htno, phone, password, **other_fields):
        if not email or len(email) == 0:
            raise ValueError(_('You must provide an email address'))
        if not re.match(EMAIL_FORMAT, email):
            raise ValueError(_('You must provide valid organization email'))
        if not first_name or len(first_name) == 0:
            raise ValueError(_('You must provide a first name'))
        if not last_name or len(last_name) == 0:
            raise ValueError(_('You must provide a last name'))
        if not user_name or len(user_name) == 0:
            raise ValueError(_('You must provide an username'))
        if not dob:
            raise ValueError(_('You must provide dob'))
        if not htno or len(htno) == 0:
            raise ValueError(_('You must provide htno'))
        if not grad_year:
            raise ValueError(_('You must provide a valid grad_year'))
        if not phone or len(phone) != 10:
            raise ValueError(_('You must provide a valid phone number'))
        if not password or len(password) == 0:
            raise ValueError(_('You must provide a valid password'))
        email = self.normalize_email(email=email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, last_name=last_name,
                          dob=dob, grad_year=grad_year, htno=htno, phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, last_name, dob, grad_year, htno, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        return self.create_user(email, user_name, first_name, last_name, dob, grad_year, htno, phone, password, **other_fields)
