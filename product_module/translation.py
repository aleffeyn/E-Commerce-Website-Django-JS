from modeltranslation.translator import TranslationOptions, register

from product_module.models import Product, ProductCategory, ProductBrand, ProductTag


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "description")


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(ProductBrand)
class ProductBrandTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(ProductTag)
class ProductTagTranslationOptions(TranslationOptions):
    fields = ("caption",)
