from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.crypto import get_random_string
from django.views import View

from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from utils.email_service import send_email
from .models import User
from django.contrib.auth import login,logout


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request , 'account_module/register_page.html' , {'register_form': register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()

            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(length=72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                # todo: send email activation code
                send_email('فعالسازی حساب کاربری',new_user.email,{'user' : new_user},'emails/account_activation.html')
                return redirect(reverse('login_page'))

        return render(request , 'account_module/register_page.html' , {'register_form': register_form})

class ActivateAccountView(View):
    def get(self, request, email_activation_code):
        user = User.objects.filter(email_active_code__iexact=email_activation_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.save()
                user.email_active_code = get_random_string(length=72)
                #todo: show success message
                return redirect('login_page')
            else:
                #todo: show error message
                pass


        raise Http404

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        next_url = request.GET.get('next', '')
        return render(request, 'account_module/login_page.html', {
            'login_form': login_form,
            'next': next_url
        })
    def post(self, request):
        login_form = LoginForm(request.POST)
        next_url = request.POST.get('next', '')
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email','حساب کاربری فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        if next_url and url_has_allowed_host_and_scheme(
                                url=next_url,
                                allowed_hosts={request.get_host()},
                                require_https=request.is_secure()
                        ):
                            return redirect(next_url)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password','گذرواژه وارد شده اشتباه میباشد')
            else:
                login_form.add_error('email' , 'ایمیل وارد شده اشتباه می باشد')

        context = {'login_form': login_form, 'next': next_url}
        return render(request, 'account_module/login_page.html', context)

class ForgotPasswordView(View):
    def get(self , request):
        forgot_password_form = ForgotPasswordForm()
        return render(request, 'account_module/forgot_pass_page.html' , {'forgot_password_form': forgot_password_form})
    def post(self, request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=email).first()
            if user is not None:
                #todo: send email
                send_email('بازیابی کلمه عبور',user.email,{'user' : user},'emails/forgot_password.html')
                return redirect(reverse('login_page'))
            else:
                forgot_password_form.add_error('email' , 'کاربری با ایمیل وارد شده یافت نشد')
        return render(request, 'account_module/forgot_pass_page.html' , {'forgot_password_form': forgot_password_form})

class ResetPasswordView(View):
    def get(self, request, activation_code):
        user = User.objects.filter(email_active_code__iexact=activation_code).first()
        if user is None:
            raise Http404
        reset_password_form = ResetPasswordForm()
        return render(request, 'account_module/reset_pass_page.html' , {
            'reset_password_form': reset_password_form,
            'user': user,
        })
    def post(self, request, activation_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user = User.objects.filter(email_active_code__iexact=activation_code).first()
        if reset_password_form.is_valid():
            if user is None:
                raise Http404
            new_password = reset_password_form.cleaned_data.get('password')
            user.set_password(new_password)
            user.email_active_code = get_random_string(length=72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))
        return render(request, 'account_module/reset_pass_page.html' , {
            'reset_password_form': reset_password_form,
            'user': user,
        })

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))