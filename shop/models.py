from django.db import models
from django.utils.text import slugify
from django.urls import reverse

import random
import string
# Create your models here.

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)

def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

class Category(models.Model):

    name = models.CharField(verbose_name='Категория', max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse("shop:category_list", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + f'-pickBetter' + f"{self.name}")
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    title = models.CharField(verbose_name='Название', max_length=250)
    brand = models.CharField(verbose_name='Брeнд', max_length=250)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    slug = models.SlugField(verbose_name='URL', max_length=250)
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(verbose_name="Изображение", upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField(verbose_name='Наличие', default=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={'slug': self.slug})



class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy=True

