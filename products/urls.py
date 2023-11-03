from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("cart/add/<int:product_id>/", views.CartAddView.as_view(), name="cart_add"),
    path("cart/", views.CartListView.as_view(), name="cart_list"),
    path(
        "cart/update/<int:product_id>/",
        views.CartItemUpdateView.as_view(),
        name="cart_update",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.CartItemDeleteView.as_view(),
        name="cart_remove",
    ),
]
