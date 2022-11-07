from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
# force_text is depricated in django v4.0
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import Account, EmailVerification, Profile
from .backends import ExtendedUserModelBackend
from .forms import CustomUserCreationForm, LoginForm
from .token import account_activation_token

from django.core.exceptions import ObjectDoesNotExist


# def logout_request(request):
# 	logout(request)
# 	messages.info(request, "You have successfully logged out.")
# 	return redirect("accounts:home")

def profile(request):
    return render(request, template_name="accounts/home.html")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


# def login_request(request):
#     form = LoginForm(request.POST)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         try:
#             user = authenticate(username=username, password=password)
#         except ObjectDoesNotExist:
#             return messages.info(request, f"There is no user registered with{username}. Please Sign Up!.")

#         # print("username: ", username, "passowrd: ", password)
#         # print("user from authenticate :",authenticate(username=username, password=password))
#         if user is not None:
#             user.backend = "accounts.backends.ExtendedUserModelBackend"
#             login(request, user)
#             messages.info(request, f"Your are now logged in as {username}.")
#             if request.GET.__contains__('next'):
#                 return redirect(request.GET.__getitem__('next'))
#             # print("next url :", request.GET.__getitem__('next'))
#             return redirect("profile")
#         else:
#             # messages.error(request, "Please Verify your email to login.")
#             return HttpResponse("Please Verify your email to login.")
#     form = LoginForm()
#     return render(request, template_name="accounts/login.html", context={"form": form})

def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # try:
            #     user = ExtendedUserModelBackend.authenticate(username=username, password=password)
            # except Exception as e:
            #     print("Exception ->>> ",e)
            #     messages.warning(request, f"We do not have user registered with {username}, please Sign Up!.")
            #     reverse('signup') # take him to sign up page
            user = ExtendedUserModelBackend.authenticate(request, username=username, password=password)
            print(f"user == {user}")
            if user is not None:
                user.backend = "accounts.backends.ExtendedUserModelBackend"
                if ExtendedUserModelBackend.user_can_authenticate(request, username=username, password=password):
                    login(request, user)
                    messages.info(request, f"Your are now logged in as {username}.")
                    if request.GET.__contains__('next'):
                        print("next url :", request.GET.__getitem__('next'))
                        return redirect(request.GET.__getitem__('next'))
                    return redirect("profile")
                else:
                    messages.warning(request, f"Please correct your username and password.")
                    reverse('login') # take him to sign up page
            else:
                # return HttpResponse("Please check your ID and password and try again!!.")
                messages.warning(request, f"We do not have user registered with {username}, please Sign Up!.")
                reverse('signup') # take him to sign up page
    else:
        form = LoginForm()
    return render(request, template_name="accounts/login.html", context={"form": form})


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # form = CustomUserCreationForm(request.POST)
        print("form data = ",form.cleaned_data.get("username"))
        if form.is_valid():
            user = form.save(commit=False)
            print("user :",user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # print("current site :", current_site)
            mail_subject = 'Activate your  blizzard account.'
            mail_message = render_to_string('accounts/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data['email']
            email = EmailMessage(mail_subject, mail_message, to=[to_email])
            email.send()
            print("Mail Sent to user ",to_email)
            # messages.success(request, "Registration successful.")
            return HttpResponse('Please verify your email to complete the registration.')
        messages.error(request, "Unsuccessfull registration, Invalid information for user.")
        HttpResponse('Please verify your email to .')
    form = CustomUserCreationForm()
    return render(request, template_name='accounts/signup.html', context={"form": form})

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True
        EmailVerification.objects.filter(user=user).update(verified=True)
        Profile.objects.create(user=user, image='media/default.jpg')
        print("user is activated now.")  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  