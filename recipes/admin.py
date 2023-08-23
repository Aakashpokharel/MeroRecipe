# recipes/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe, Rating
from django.db.models import Avg


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "recipe_name",
        "get_ingredients",
        "get_instructions",
        "cuisine",
        "cooking_time",
        "difficulty_level",
        "image",
        "user",
    )
    list_filter = ("cuisine", "cooking_time", "difficulty_level", "image")
    search_fields = ("recipe_name", "cuisine")

    def get_ingredients(self, obj):
        ingredients_list = obj.ingredients
        ingredients_html = "<ul>"
        for ingredient in ingredients_list.split("\n"):
            ingredients_html += f"<li>{ingredient}</li>"
        ingredients_html += "</ul>"
        return format_html(ingredients_html)

    def get_instructions(self, obj):
        instructions_text = obj.instructions
        instructions_html = "<ol>"
        for step in instructions_text.split("\n"):
            instructions_html += f"<li>{step}</li>"
        instructions_html += "</ol>"
        return format_html(instructions_html)

    get_ingredients.short_description = "Ingredients"
    get_instructions.short_description = "Instructions"


class RatingAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "recipe",
        "rating",
        "created_at",
    ]
    list_filter = ["user", "recipe"]
    search_fields = ["user__username", "recipe__title"]


admin.site.register(Rating, RatingAdmin)
admin.site.register(Recipe, RecipeAdmin)
