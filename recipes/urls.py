from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "recipe"

urlpatterns = [
    path("", views.LandingPage.as_view(), name="home"),
    path("share-recipe/", views.ShareRecipe.as_view(), name="share-recipe"),
    path("recipe-list/", views.RecipeListView.as_view(), name="recipe-list"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipe-create/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path(
        "<int:pk>/update/",
        views.RecipeUpdateView.as_view(),
        name="recipe-update",
    ),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
    path("<int:pk>/rate/", views.RatingCreateView.as_view(), name="rate-recipe"),
    path(
        "<int:pk>/update-rating/",
        views.RatingUpdateView.as_view(),
        name="update-rating",
    ),
    path(
        "<int:pk>/delete-rating/",
        views.RatingDeleteView.as_view(),
        name="delete-rating",
    ),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
