from django import forms
from .models import Product, CartItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "quantity", "image"]

    # Add Bootstrap classes to form fields
    widgets = {
        "name": forms.TextInput(attrs={"class": "form-control"}),
        "description": forms.Textarea(attrs={"class": "form-control"}),
        "price": forms.NumberInput(attrs={"class": "form-control"}),
        "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        "image": forms.FileInput(attrs={"class": "form-control-file"}),
    }

    def clean_image(self):
        image = self.cleaned_data.get("image", False)
        if not image and self.instance:
            # If no new image is provided during update, return the current instance's image
            return self.instance.image
        return image


class CartItemUpdateForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["quantity"]
