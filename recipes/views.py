from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy


# Create your views here.
class LandingPage(TemplateView, LoginRequiredMixin):
    template_name = "home.html"
    login_url = reverse_lazy("login")

    def handle_no_permission(self):
        return redirect(self.login_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ShareRecipe(LoginRequiredMixin, TemplateView):
    template_name = "recipe/share-recipe.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
