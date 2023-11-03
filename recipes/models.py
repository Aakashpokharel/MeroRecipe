from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


# Create your models here.


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Intermediate", "Intermediate"),
        ("Difficult", "Difficult"),
    ]

    recipe_name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    cuisine = models.CharField(max_length=100)
    cooking_time = models.CharField(max_length=50)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.recipe_name


class Interaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


class RecipeVisit(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


# For Image
@receiver(pre_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    # Check if the recipe has an associated image
    if instance.image:
        # Delete the image from the media storage
        instance.image.delete(save=False)


@receiver(pre_save, sender=Recipe)
def delete_previous_recipe_image(sender, instance, **kwargs):
    # Check if the instance is being updated and has a primary key (already saved in the database)
    if instance.pk and Recipe.objects.filter(pk=instance.pk).exists():
        # Retrieve the existing instance from the database
        existing_instance = Recipe.objects.get(pk=instance.pk)

        # Check if the image has changed (i.e., a new image has been uploaded)
        if instance.image and instance.image != existing_instance.image:
            # Delete the previous image
            existing_instance.image.delete(save=False)


# Connect the signal handlers to the respective signals
pre_delete.connect(delete_recipe_image, sender=Recipe)
pre_save.connect(delete_previous_recipe_image, sender=Recipe)


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
