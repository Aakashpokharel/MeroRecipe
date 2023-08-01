from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.views.generic import FormView


CustomUser = get_user_model()


class IndexView(TemplateView):
    template_name = "home.html"


class UserView(LoginRequiredMixin, TemplateView):
    template_name = "user/user.html"


class Registration(FormView):
    template_name = "user/user_registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.is_user = True
        form.save()
        return super().form_valid(form)


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        context = {
            "username": username,
        }

        if username == "":
            messages.error(request, "Please Enter username")
            return render(request, "login.html", context=context)

        if password == "":
            messages.error(request, "Please Enter Password")
            return render(request, "login.html", context=context)

        user = username == username and password == password
        if user:
            user = auth.authenticate(username=username, password=password)

            if user:
                if not user.is_active and user.is_user:
                    messages.error(request, "Please Activate Account.")
                    return render(request, "login.html")
                elif user.is_active and user.is_user:
                    auth.login(request, user)
                    messages.success(
                        request,
                        "Welcome, " + user.username + ". You are now logged in.",
                    )
                    return redirect("user-dash")
            else:
                messages.error(request, "Invalid credentials")
                return render(request, "login.html", context=context)

        else:
            messages.error(request, "Something went wrong.")
            return render(request, "login.html", context=context)


class Logout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "Logged Out")
        return redirect("login")
