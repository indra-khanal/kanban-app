import re
def validate_email_address(email_address):
   if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", email_address):
       return False
   else:
       return True