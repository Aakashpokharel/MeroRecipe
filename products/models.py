from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    vendor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    # Check if the product has an associated image
    if instance.image:
        # Delete the image from the media storage
        instance.image.delete(save=False)


@receiver(pre_save, sender=Product)
def delete_previous_product_image(sender, instance, **kwargs):
    # Check if the instance is being updated and has a primary key (already saved in the database)
    if instance.pk and Product.objects.filter(pk=instance.pk).exists():
        # Retrieve the existing instance from the database
        existing_instance = Product.objects.get(pk=instance.pk)

        # Check if the image has changed (i.e., a new image has been uploaded)
        if instance.image and instance.image != existing_instance.image:
            # Delete the previous image
            existing_instance.image.delete(save=False)


# Connect the signal handlers to the respective signals
pre_delete.connect(delete_product_image, sender=Product)
pre_save.connect(delete_previous_product_image, sender=Product)
