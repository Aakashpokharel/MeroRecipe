from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm

# from .forms import UserRegistrationForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "is_user", "is_vendor")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_vendor",
                    "is_user",
                ),
            },
        ),
    )

    list_display = ["username", "email", "is_staff", "is_vendor", "is_user"]
    list_filter = ["is_staff", "is_superuser", "is_active", "is_vendor", "is_user"]
    search_fields = ["username", "email"]


admin.site.register(CustomUser, CustomUserAdmin)
