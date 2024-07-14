import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import DateFieldsMixin


class MenuCategory(DateFieldsMixin, models.Model):
    label = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, allow_unicode=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.label, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('menu-category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.label


class MenuItem(DateFieldsMixin, models.Model):
    def food_image_upload_to(self, filename):
        return f"menu_item_images/{self.menu_category}/{filename}"

    food_name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(max_length=100, blank=True, null=True, allow_unicode=True)

    description = models.CharField(max_length=200, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[
            MaxValueValidator(1.0),
            MinValueValidator(0.0),
        ])
    inventory = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(
        upload_to=food_image_upload_to,
        default='default_food_image.jpg',
        blank=True
    )
    menu_category = models.ForeignKey(
        MenuCategory,
        on_delete=models.PROTECT,  # It's needed for directory name
        related_name='menu_items'
    )

    def __str__(self):
        return self.food_name

    @property
    def discounted_price(self):
        return round(self.price * (1 - self.discount))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.food_name, allow_unicode=True)
            unique_slug = self.slug
            num = 1
            while MenuItem.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args,
                     **kwargs)

    def get_absolute_url(self):
        return reverse('menu-category', kwargs={'slug': self.menu_category.slug})
        # return reverse('menu-category', kwargs={'selected_category': self.slug})
        # TODO:NEED VIEW FOR ITEMS OR BE HANDLED ON SELECTED CATEGORY


@receiver(post_delete, sender=MenuItem)
def delete_menu_item_image(sender, instance: MenuItem, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_save, sender=MenuItem)
# TODO: Move the image directory if the category changed
# TODO: Remove the category directory in MEDIA_ROOT if the category is deleted
def delete_old_menu_item_image(sender, instance: MenuItem, **kwargs):
    if not instance.id:
        return False

    try:
        old_instance = MenuItem.objects.get(id=instance.id)
    except MenuItem.DoesNotExist:
        return False

    if instance.image != old_instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)
