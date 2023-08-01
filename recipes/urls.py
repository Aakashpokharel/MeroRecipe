from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingPage.as_view(), name="home"),
    path("share-recipe/", views.ShareRecipe.as_view(), name="share-recipe"),
]
