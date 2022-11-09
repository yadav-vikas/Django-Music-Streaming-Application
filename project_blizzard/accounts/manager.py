from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **other_fields):

        if not email:
            raise ValueError("You must specify valid Email!")
        if not username:
            raise ValueError("You must specify valid username!")
        # elif username and not username.isspace(): # code
        #     print("the username is valid.")
        # else: 
        #     username = email
        #     print("using username as email.")

        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **other_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, username, password=None, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("superusermust be assigned to is_staff=True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("superusermust be assigned to is_superuser=True")

        # return self.create_user(username, email, password, **other_fields)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password=password, **other_fields)
        user.set_password(password)
        # user.is_active = True
        # user.EmailVerification.verified = True
        user.is_admin = True
        user.save(using=self._db)
        return user