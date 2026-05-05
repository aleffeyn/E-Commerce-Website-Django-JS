import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop_project.settings")

import django

django.setup()

from article_module.models import Article, ArticleCategory
from product_module.models import Product, ProductBrand, ProductCategory
from site_module.models import Banner, FooterLink, FooterLinkBox, SiteSetting, Slider


FA_MAP = {
    "mobile": "موبایل",
    "home-stuff": "لوازم خانگی",
    "washing-machine": "ماشین لباسشویی",
    "clothing": "پوشاک",
    "digital": "دیجیتال",
    "apple": "اپل",
    "samsung": "سامسونگ",
    "xiaomi": "شیائومی",
}

EN_MAP = {
    "موبایل": "Mobile",
    "لوازم خانگی": "Home Appliances",
    "ماشین لباسشویی": "Washing Machine",
    "پوشاک": "Clothing",
    "دیجیتال": "Digital",
    "اپل": "Apple",
    "سامسونگ": "Samsung",
    "شیائومی": "Xiaomi",
}

IT_MAP = {
    "موبایل": "Cellulare",
    "لوازم خانگی": "Elettrodomestici",
    "ماشین لباسشویی": "Lavatrice",
    "پوشاک": "Abbigliamento",
    "دیجیتال": "Digitale",
    "اپل": "Apple",
    "سامسونگ": "Samsung",
    "شیائومی": "Xiaomi",
}


def clean_text(value):
    return (value or "").strip()


def slug_to_title(value):
    return clean_text(value).replace("-", " ").replace("_", " ").title()


def fill_triple(obj, field, fallback=""):
    fa_field = f"{field}_fa"
    en_field = f"{field}_en"
    it_field = f"{field}_it"

    fa_value = clean_text(getattr(obj, fa_field, ""))
    en_value = clean_text(getattr(obj, en_field, ""))
    it_value = clean_text(getattr(obj, it_field, ""))

    source = clean_text(getattr(obj, field, "")) or clean_text(fallback)
    map_key = clean_text(fallback).lower()
    fa_from_map = FA_MAP.get(map_key, "")

    if not fa_value and (source or fa_from_map):
        fa_value = fa_from_map or source
        setattr(obj, fa_field, fa_value)

    if not en_value and fa_value:
        setattr(obj, en_field, EN_MAP.get(fa_value, fa_value))

    if not it_value and fa_value:
        setattr(obj, it_field, IT_MAP.get(fa_value, EN_MAP.get(fa_value, fa_value)))


updated = 0

for obj in ProductCategory.objects.all():
    fill_triple(obj, "title", fallback=obj.url_title)
    obj.save()
    updated += 1

for obj in ProductBrand.objects.all():
    fill_triple(obj, "title", fallback=obj.url_title)
    obj.save()
    updated += 1

for obj in Product.objects.all():
    fill_triple(obj, "title", fallback=obj.slug)
    fill_triple(obj, "description", fallback=obj.slug)
    fill_triple(obj, "short_description", fallback=obj.slug)
    obj.save()
    updated += 1

for obj in ArticleCategory.objects.all():
    fill_triple(obj, "title", fallback=obj.url_title)
    obj.save()
    updated += 1

for obj in Article.objects.all():
    fill_triple(obj, "title", fallback=obj.slug)
    fill_triple(obj, "short_description", fallback=obj.slug)
    fill_triple(obj, "content", fallback=obj.slug)
    obj.save()
    updated += 1

for obj in SiteSetting.objects.all():
    fill_triple(obj, "site_name", fallback="eshop")
    fill_triple(obj, "address")
    fill_triple(obj, "about_us_text")
    fill_triple(obj, "copy_right")
    obj.save()
    updated += 1

for obj in FooterLinkBox.objects.all():
    fill_triple(obj, "title")
    obj.save()
    updated += 1

for obj in FooterLink.objects.all():
    fill_triple(obj, "title")
    obj.save()
    updated += 1

for obj in Slider.objects.all():
    fill_triple(obj, "title")
    fill_triple(obj, "sub_title")
    fill_triple(obj, "url_title")
    obj.save()
    updated += 1

for obj in Banner.objects.all():
    fill_triple(obj, "title")
    obj.save()
    updated += 1

print(f"Updated translation fields on {updated} rows.")
