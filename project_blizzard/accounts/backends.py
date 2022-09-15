from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .manager import CustomAccountManager

UserModel = get_user_model()


class ExtendedUserModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # n.b. Django <2.1 does not pass the `request`

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        # The `username` field is allows to contain `@` characters so
        # technically a given email address could be present in either field,
        # possibly even for different users, so we'll query for all matching
        # records and test each one.
        users = user_model._default_manager.filter(
            (Q(**{user_model.USERNAME_FIELD: username}) | (Q(email__exact=username)))
        )

        # Test whether any matched user has the provided password:
        for user in users:
            print("user_verification :",user.verify.verified)
            if user.check_password(password) & user.verify.verified == True:
                print("this is a verified user")
                return user
            # else:
            #     return HttpResponse("please check your email and verify your identity.")
        if not users:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (see
            # https://code.djangoproject.com/ticket/20760)
            user_model().set_password(password)
        return user

    def get_user(self, user_id=None):
        # UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
