from django.db import models

# Create your models here.


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='Site Name')
    site_url = models.CharField(max_length=200, verbose_name='Site URL')
    email = models.CharField(verbose_name='Site Email')
    phone = models.CharField(max_length=20, verbose_name='Site Phone Number')
    address = models.TextField(verbose_name='Site Address')
    fax = models.CharField(max_length=20, verbose_name='Site Fax')
    logo = models.ImageField(upload_to='images/site_setting', verbose_name='Site Logo')
    copy_right = models.TextField(verbose_name='Site Copy Right')
    about_us_text = models.TextField(verbose_name='About Us')
    is_main_setting = models.BooleanField(default=True, verbose_name='Main Site Setting')

    def __str__(self):
        return self.site_name
    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='Footer Link Box Title')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Footer Link Box'
        verbose_name_plural = 'Footer Link Boxes'

class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    url = models.URLField(verbose_name='URL')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='Category')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Footer Link'
        verbose_name_plural = 'Footer Links'

class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='Slider Title')
    sub_title = models.CharField(max_length=200, verbose_name='Slider Sub Title')
    url = models.URLField(max_length=500 ,verbose_name='Slider URL')
    url_title = models.CharField(max_length=200, verbose_name='Slider URL Title')
    image = models.ImageField(upload_to='images/slider', verbose_name='Slider Image')
    is_active = models.BooleanField(default=True, verbose_name='Slider Status')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'

class Banner(models.Model):
    class BannerPosition(models.TextChoices):
        product_list = 'product_list'
        product_detail = 'product_detail'

    title = models.CharField(max_length=200, verbose_name='Banner Title')
    url = models.URLField(max_length=500 ,verbose_name='Banner URL')
    image = models.ImageField(upload_to='images/banner', verbose_name='Banner Image')
    position = models.CharField(max_length=20, choices=BannerPosition.choices, verbose_name='Banner Position')
    is_active = models.BooleanField(default=True, verbose_name='Banner Status')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Advertising Banner'
        verbose_name_plural = 'Advertising Banners'