from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at", "updated_at")
    list_filter = ("category", "price", "created_at")
    search_fields = ("name", "description")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("reviewer", "product__name", "comment")

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ("user", "created_at")
#     search_fields = ("user__username",)

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ("cart", "product", "quantity", "added_at")
#     list_filter = ("added_at",)
#     search_fields = ("cart__user__username", "product__name")