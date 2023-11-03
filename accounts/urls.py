from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.IndexView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.Registration.as_view(), name="signup"),
    path("user-dashboard/", views.UserView.as_view(), name="user-dash"),
    path("vendor-dashboard/", views.UserView.as_view(), name="vendor-dash"),
    path("logout", views.Logout.as_view(), name="logout"),
]
