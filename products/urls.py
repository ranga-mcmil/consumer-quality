from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("cart/", views.CartDetailView.as_view(), name="cart-detail"),
    path("cart/add/<int:product_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.RemoveFromCartView.as_view(), name="remove_from_cart"),

    path("checkout/", views.CheckoutView.as_view(), name="checkout"),

    path("search/", views.ProductSearchView.as_view(), name="search"),

]