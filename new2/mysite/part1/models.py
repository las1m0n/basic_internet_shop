from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.urls import reverse
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_view', kwargs={'category_slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


def image_folder(instance, filename):
    filename = instance.slug + "." + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Product(models.Model):
    category = models.ForeignKey(Category, True)
    brand = models.ForeignKey(Brand, True)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = RichTextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    compare = models.ManyToManyField(User, related_name='compare', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_view', kwargs={'product_slug': self.slug})


class CartItem(models.Model):
    product = models.ForeignKey(Product, True)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart item {self.product.title}"


class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)

    def add_to_cart(self, slug):
        cart = self
        product = Product.objects.get(slug=slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()

    def remove_from_cart(self, slug):
        cart = self
        product = Product.objects.get(slug=slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def remove_all_cart(self):
        cart = self
        cart.items.clear()
        cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


ORDER_STATUS_CHOICES = (
    ('Принят в обработку', 'Принят в обработку'),
    ('Выполняется', 'Выполняется'),
    ('Оплачен', 'Оплачен')
)


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, True)
    items = models.ForeignKey(Cart, True)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    buying_type = models.CharField(max_length=40, choices=(('Самовывоз', 'Самовывоз'), ('Доставка курьером',
                                                                                        'Доставка курьером')),
                                   default='Самовызов')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return f"Заказ номер --> {self.id}"


class Relation(models.Model):
    slug = models.SlugField()
    product = models.ForeignKey(Product, True)
    relations = models.ManyToManyField(Product, related_name='relationss', blank=True, null=True)

