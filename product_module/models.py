from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ProductCategory(models.Model):
    title = models.CharField(max_length=200 , verbose_name='Category Name', db_index=True)
    url_title = models.CharField(max_length=200 , verbose_name='Category URL Title')
    category = models.ForeignKey('self' , on_delete=models.CASCADE , null=True , blank=True)
    is_active = models.BooleanField(verbose_name='Category Status')
    is_delete = models.BooleanField(verbose_name='Product Delete Status')


    def __str__(self):
        return f'({self.title} - {self.url_title})'

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

class ProductBrand(models.Model):
    title = models.CharField(max_length=200 , verbose_name='Brand Name', db_index=True)
    url_title = models.CharField(max_length=200 , verbose_name='Brand URL Title', db_index=True)
    is_active = models.BooleanField(verbose_name='Brand Status')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product Brand'
        verbose_name_plural = 'Product Brands'

class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(
        ProductCategory,
        related_name='product_categories', verbose_name='Categories'
    )
    image = models.ImageField(upload_to='images/products', verbose_name='Product Image', null=True , blank=True)
    brand = models.ForeignKey(ProductBrand , on_delete=models.CASCADE , related_name='product_brands' , null=True , blank=True)
    price = models.IntegerField(verbose_name='Product Price')
    short_description = models.CharField(max_length=360 , null=True, verbose_name='Product Short Description')
    description = models.TextField(verbose_name='Product Description')
    is_active = models.BooleanField(default=False, verbose_name='Product Status')
    slug = models.SlugField(default='' , null=False , db_index=True , blank=True, max_length=200, unique=True)
    is_delete = models.BooleanField(verbose_name='Product Delete Status')


    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args , **kwargs)

    def __str__(self):
        return f'{ self.title} - {self.price}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductTag(models.Model):
    products = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product_tags')
    caption = models.CharField(max_length=200, db_index=True , verbose_name='Tag Caption')


    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'Product Tag'
        verbose_name_plural = 'Products Tags'

class ProductVisit(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name='Related Product')
    ip = models.CharField(max_length=200 , verbose_name='IP Address')
    user = models.ForeignKey('account_module.User' , on_delete=models.CASCADE , null=True , blank=True, verbose_name='User')

    class Meta:
        verbose_name = 'Product Visit'
        verbose_name_plural = 'Product Visits'

    def __str__(self):
        return f'{self.product.title} - {self.ip}'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='Product')
    image = models.ImageField(upload_to='images/products/gallery', verbose_name='Gallery Image')
    image_alt = models.CharField(max_length=200, blank=True, null=True, verbose_name='Image Alt Text')
    is_main = models.BooleanField(default=False, verbose_name='Main Image')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Gallery Image'
        verbose_name_plural = 'Product Gallery Images'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.product.title} - Image {self.order}'

    def save(self, *args, **kwargs):
        # If this image is set as main, unset other main images for this product
        if self.is_main:
            ProductGallery.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
