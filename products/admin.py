from django.contrib import admin
from .models import Product
from accounts.models import CustomUser


# Register your models here.
@admin.register(Product)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity", "image", "vendor")
    list_filter = ("vendor",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vendor":
            kwargs["queryset"] = CustomUser.objects.filter(is_vendor=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
