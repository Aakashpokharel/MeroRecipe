# views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Product, Cart, CartItem
from .forms import ProductForm, CartItemUpdateForm
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


# restricting user
class IsUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_vendor


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10  # Optional: Specify the number of products per page

    def get_queryset(self):
        # Filter products based on the logged-in vendor
        return Product.objects.filter(vendor=self.request.user)


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, IsUserMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        # Check if the logged-in user is a vendor (is_vendor is True)
        if self.request.user.is_vendor:
            form.instance.vendor = (
                self.request.user
            )  # Assign the logged-in user as the vendor
            return super().form_valid(form)
        else:
            # Handle the case where the user is not a vendor
            # You can display an error message or take appropriate action
            # For example, you can redirect to a page indicating that the user is not a vendor
            return HttpResponse("You are not authorized to create products.")


class ProductUpdateView(LoginRequiredMixin, IsUserMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        # Check if the logged-in user is a vendor (is_vendor is True)
        if self.request.user.is_vendor:
            form.instance.vendor = (
                self.request.user
            )  # Assign the logged-in user as the vendor
            return super().form_valid(form)
        else:
            # Handle the case where the user is not a vendor
            # You can display an error message or take appropriate action
            # For example, you can redirect to a page indicating that the user is not a vendor
            return HttpResponse("You are not authorized to update products.")


class ProductDeleteView(LoginRequiredMixin, IsUserMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy(
        "product_list"
    )  # Redirect to the product list after successful delete


# For Cart
class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect(reverse("cart_list"))


class CartListView(ListView):
    model = Cart
    template_name = "cart/cart_list.html"
    context_object_name = "cart_items"


class CartItemUpdateView(UpdateView):
    model = CartItem
    form_class = CartItemUpdateForm
    template_name = "cart/cart_form.html"
    fields = ["quantity"]

    def get_object(self, queryset=None):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        cart = (
            self.request.user.cart
        )  # Assuming you have a way to associate the cart with the user
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        return cart_item

    def get_success_url(self):
        return reverse("cart_list")


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = "cart/cart_confirm_delete.html"
    success_url = "/cart/"
