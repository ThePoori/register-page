from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpResponse
from django.shortcuts import render

from account.forms import RegisterForm


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact = user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(email = user_email,
                                email_active_code = get_random_string(72),
                                is_active=False,
                                username = user_email)
                new_user.set_password(user_password)
                new_user.save()
                # todo : send email active code
                return render(request, 'account/register_success.html', {'register_form': register_form})


        context = {
            'register_form': register_form
        }
        return render(request, 'account/register.html', context)
    

class LoginView(View):
    def get(self, request):
        context = {
            'login_form': None
        }
        return render(request, 'account/register.html', context)
    def post(self, request):
        pass


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user : User = User.objects.filter(email_active_code__iexact = email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return render(request, 'account/account_verified.html')
        else:
            pass
        raise Http404



