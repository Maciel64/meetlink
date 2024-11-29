from django.contrib.auth.models import User


def get_user_by_email(email: str) :
  return User.objects.get(email = email)