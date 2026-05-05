from django import forms
from django.utils.translation import gettext_lazy as _

from contact_module.models import Contact


# class ContactUsForm(forms.Form):
#     full_name = forms.CharField(
#         label='نام و نام خانوادگی',
#         max_length=50,
#         widget=forms.TextInput(
#             attrs=
#             {
#             'class': 'form-control',
#             'placeholder' : 'نام و نام خانوادگی'
#             }),
#         error_messages={
#             'required' : 'لطفا نام و نام خانوادگی خود را وارد کنید',
#             'max_length' : 'لطفا بیشتر از 50 کاراکتر وارد نکنید'
#         }
#     )
#     email = forms.EmailField(
#         label='ایمیل',
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'ایمیل'
#         }),
#         error_messages={
#             'required': 'لطفا ایمیل خود را وارد کنید',
#         }
#     )
#     subject = forms.CharField(
#         label='عنوان',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder' : 'عنوان'
#         }),
#         error_messages={
#             'required': 'لطفا عنوان را بنویسید ',
#         },
#         max_length=100
#     )
#     message = forms.CharField(
#         label='پیام شما',
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder' : 'پیام شما',
#             'id': 'message'
#         }),
#         error_messages={
#             'required': 'لطفا پیام خود را بنویسید',
#         }
#     )

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name' , 'email' , 'title' , 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('نام و نام خانوادگی')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('ایمیل')
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('عنوان')
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'message',
                'placeholder': _('پیام شما'),
                'rows': '5'
            }),
        }
        labels = {
            'name' : _('نام و نام خانوادگی '),
            'email' : _('ایمیل '),
            'title' : _('عنوان'),
            'message' : _('پیام شما')
        }
        error_messages = {
            'name' : {
                'required' : _('پر کردن این فیلد الزامی میباشد'),
                'max_length' : _('بیشتر از 50 کاراکتر وارد نکنید')
            },
            'email': {
                'required': _('پر کردن این فیلد الزامی میباشد')
            },
            'title': {
                'required': _('پر کردن این فیلد الزامی میباشد')
            },
            'message': {
                'required': _('پر کردن این فیلد الزامی میباشد')
            }
        }
