# Generated by Django 4.2.3 on 2023-08-06 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_alter_recipe_ingredients_alter_recipe_instructions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="instructions",
            field=models.TextField(),
        ),
    ]