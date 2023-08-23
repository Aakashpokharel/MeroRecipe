from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Recipe, Rating
from .forms import RecipeForm, RatingForm
from django.db.models import Avg
from math import floor


# Create your views here.
class RecipeOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user


class LandingPage(TemplateView, LoginRequiredMixin):
    model = Recipe
    template_name = "home.html"

    paginate_by = 12

    login_url = reverse_lazy("login")

    def handle_no_permission(self):
        return redirect(self.login_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    context_object_name = "recipes"


class ShareRecipe(LoginRequiredMixin, TemplateView):
    template_name = "recipe/share-recipe.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class RecipeListView(LoginRequiredMixin, ListView, RecipeOwnerMixin):
    model = Recipe
    template_name = "recipe/recipe_list.html"
    context_object_name = "recipes"


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipe/recipe_form.html"
    form_class = RecipeForm
    success_url = reverse_lazy("recipe:recipe-list")

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the logged-in user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Recipe
    template_name = "recipe/recipe_form.html"
    form_class = RecipeForm
    success_url = reverse_lazy("recipe:recipe-list")

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user

    def form_valid(self, form):
        recipe = form.save(commit=False)
        if not form.cleaned_data["image"]:
            # If image field is empty, retain the existing image
            recipe.image = self.get_object().image
        recipe.save()
        return super().form_valid(form)


class RecipeDetailView(LoginRequiredMixin, DetailView, UserPassesTestMixin):
    model = Recipe
    template_name = "recipe/recipe_detail.html"
    context_object_name = "recipe"

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user

    def calculate_stars(self, rating):
        full_stars = int(rating)  # Take integer part
        decimal_part = rating - full_stars  # Calculate decimal part
        if decimal_part >= 0.75:
            full_stars += 1  # Round up to the nearest full star
            half_star = 0
        elif decimal_part >= 0.25:
            half_star = 1  # Use half star
        else:
            half_star = 0

        return full_stars, half_star

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        user = self.request.user
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=user)
            context["rating"] = user_rating
        except Rating.DoesNotExist:
            context[
                "rating_form"
            ] = RatingForm()  # Replace with your actual rating form

        context["created_by"] = recipe.user
        context["review_count"] = Rating.objects.filter(recipe=recipe).count()
        context["average_rating"] = Rating.objects.filter(recipe=recipe).aggregate(
            Avg("rating")
        )["rating__avg"]

        average_rating_dict = Rating.objects.filter(recipe=recipe).aggregate(
            Avg("rating")
        )
        average_rating = average_rating_dict["rating__avg"]
        if average_rating is not None:
            full_stars, half_star = self.calculate_stars(average_rating)
        else:
            full_stars, half_star = 0, 0  # No ratings yet, set default values
        context["full_stars"] = full_stars
        context["half_star"] = half_star

        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView, RecipeOwnerMixin):
    model = Recipe
    template_name = "recipe/recipe_confirm_delete.html"
    success_url = reverse_lazy("recipe:recipe-list")
    context_object_name = "recipe:recipe-detail"


class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = (
        "recipe/recipe_detail.html"  # Use the same template as RecipeDetailView
    )

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs["pk"])
        existing_rating = Rating.objects.filter(
            recipe=recipe, user=self.request.user
        ).first()

        if existing_rating:
            # User already submitted a rating and review, update them
            existing_rating.rating = form.cleaned_data["rating"]
            existing_rating.review = form.cleaned_data["review"]
            existing_rating.save()
        else:
            # User hasn't submitted a rating yet, create a new one
            form.instance.user = self.request.user
            form.instance.recipe = recipe
            return super().form_valid(form)

    def get_success_url(self):
        return reverse("recipe:recipe-detail", args=[str(self.kwargs["pk"])])


class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = (
        "recipe/recipe_detail.html"  # Use the same template as RecipeDetailView
    )
    success_url = reverse_lazy("recipe:recipe-detail")

    def get_object(self, queryset=None):
        return get_object_or_404(
            Rating, user=self.request.user, recipe=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating"] = self.get_object()  # Add the Rating instance to context
        context["recipe"] = context["rating"].recipe  # Add the associated recipe
        raise Exception("Rating PK: {}".format(context["rating"].pk))
        return context

    def get_success_url(self):
        return reverse("recipe:recipe-detail", args=[str(self.kwargs["pk"])])


class RatingDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Rating

    def test_func(self):
        rating = self.get_object()
        return self.request.user == rating.user

    def get_success_url(self):
        # Get the primary key of the associated recipe
        recipe_pk = self.object.recipe.pk
        return reverse("recipe:recipe-detail", args=[str(recipe_pk)])
