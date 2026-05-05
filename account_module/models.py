from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/avatars', null=True, blank=True, verbose_name=_('Avatar'))
    email_active_code = models.CharField(max_length=100, verbose_name=_('Email Active Code'))
    about_user = models.TextField(verbose_name=_('About User'), null=True, blank=True)
    address = models.TextField(verbose_name=_('User Address'), null=True, blank=True)



    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return f'{self.first_name} {self.last_name}'
        return self.username
