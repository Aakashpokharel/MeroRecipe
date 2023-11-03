from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login
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


class VendorView(LoginRequiredMixin, TemplateView):
    template_name = "vendor/vendor.html"


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
        username = request.POST.get("username")
        password = request.POST.get("password")

        context = {
            "username": username,
        }

        if not username:
            messages.error(request, "Please Enter username")
            return render(request, "login.html", context=context)

        if not password:
            messages.error(request, "Please Enter Password")
            return render(request, "login.html", context=context)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_vendor:
                    return redirect(
                        "vendor-dash"
                    )  # Redirect vendors to vendor dashboard
                else:
                    return redirect("user-dash")  # Redirect users to user dashboard
            else:
                messages.error(request, "Please Activate Account.")
        else:
            messages.error(request, "Invalid credentials")

        return render(request, "login.html", context=context)


class Logout(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "Logged Out")
        return redirect("login")
