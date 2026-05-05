from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'id': 'message'
            })
        }

        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'avatar': _('تصویر پروفایل'),
            'address': _('آدرس'),
            'about_user': _('درباره شخص'),
        }

class ChangePasswordModelForm(forms.Form):
    current_password = forms.CharField(
        label=_('کلمه عبور فعلی'),
        widget=forms.PasswordInput(attrs={'place-holder': 'Password'}),
        validators=[validators.MaxLengthValidator(20)]
    )
    new_password = forms.CharField(
        label=_('کلمه عبور جدید'),
        widget=forms.PasswordInput(attrs={'place-holder': 'Password'}),
        validators=[validators.MaxLengthValidator(20)]
    )
    confirm_new_password = forms.CharField(
        label=_('تکرار کلمه عبور جدید'),
        widget=forms.PasswordInput(attrs={'place-holder': 'Confirm Password'}),
        validators=[validators.MaxLengthValidator(20)]
    )

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError(_('کلمه عبور با تکرار کلمه عبور مغایرت دارد'))