from modeltranslation.translator import TranslationOptions, register

from site_module.models import Banner, FooterLink, FooterLinkBox, SiteSetting, Slider


@register(SiteSetting)
class SiteSettingTranslationOptions(TranslationOptions):
    fields = ("site_name", "address", "copy_right", "about_us_text")


@register(FooterLinkBox)
class FooterLinkBoxTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(FooterLink)
class FooterLinkTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ("title", "sub_title", "url_title")


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ("title",)
