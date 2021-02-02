from django.db import models


class Product(models.Model):
    owner = models.ForeignKey('accounts.User', verbose_name='owner', related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(
        'products.Category',
        verbose_name='category',
        related_name='products',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField('name', max_length=150, blank=True, null=True)
    description = models.CharField('description', max_length=2048, blank=True, null=True)
    price = models.DecimalField('price', decimal_places=2, max_digits=10, blank=True, null=True)
    quantity = models.IntegerField('quantity', blank=True, null=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Category(models.Model):
    name = models.CharField('name', max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
