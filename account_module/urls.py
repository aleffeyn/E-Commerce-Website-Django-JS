from django.contrib.auth.views import LogoutView
from django.urls import path

from account_module.views import RegisterView, LoginView, ActivateAccountView, ForgotPasswordView, ResetPasswordView, LogoutView

urlpatterns = [
    path('register/' , RegisterView.as_view() , name='register_page'),
    path('login/' , LoginView.as_view() , name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout_page'),

    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<activation_code>', ResetPasswordView.as_view(), name='reset_password'),

    path('activate_account/<email_activation_code>', ActivateAccountView.as_view(), name='activate_account')
]