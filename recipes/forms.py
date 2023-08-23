# recipes/forms.py
from django import forms
from django.forms import formset_factory
from .models import Recipe, Rating


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "recipe_name",
            "description",
            "cuisine",
            "cooking_time",
            "difficulty_level",
            "image",
            "ingredients",
            "instructions",
        ]

    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        help_text="Enter ingredients separated  by new lines (one step per line)",
    )

    instructions = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        help_text="Enter instructions separated by new lines (one step per line)",
    )

    def clean_image(self):
        image = self.cleaned_data.get("image", False)
        if not image and self.instance:
            # If no new image is provided during update, return the current instance's image
            return self.instance.image
        return image


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "review"]
        widgets = {
            "rating": forms.RadioSelect(attrs={"class": "star-rating"}),
            "review": forms.Textarea(attrs={"rows": 4}),
        }
