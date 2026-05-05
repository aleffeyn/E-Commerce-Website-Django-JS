from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=300 , verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    title = models.CharField(max_length=300 , verbose_name='Subject')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_seen = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

