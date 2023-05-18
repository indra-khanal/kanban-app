import re
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


def validate_email_address(email_address):
   if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address):
       return False
   else:
       return True
   
   
class AuthenticationFailed(APIException):
    status_code  = status.HTTP_403_FORBIDDEN
    default_detail = _('Incorrect authentication Credential')
    default_code = 'authentication_failed'