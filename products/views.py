from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, FormView
from .models import Cart, CartItem, Product, Category, Review
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import ReviewForm
from django.views.generic import TemplateView
from django.contrib import messages
from analysis import analysis as a

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category_name = self.request.GET.get("category")
        search_name = self.request.GET.get("search")

        if category_name:
            category = get_object_or_404(Category, name=category_name)
            queryset = queryset.filter(category=category)

        if search_name:
            queryset = queryset.filter(name__icontains=search_name)

        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reviews = [review.comment for review in Review.objects.filter(product=self.object)]

        result = a.yelp(reviews)


        print("")
        print("")
        print("")
        print("")
        print("result result result result result result")
        print("")
        print(result)
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")


        chart, reviews, sentiments, _rating_= result

        stars = sum(_rating_) / len(_rating_) if _rating_ else 0  

        context["chart"] = chart
        context["reviews"] = reviews
        context["sentiments"] = sentiments
        context["stars"] = range(round(stars))
        context["uncolored_stars"] = range(5 - round(stars))


        context["table"] = " "

        context["form"] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission for adding a review."""
        self.object = self.get_object()  # Ensure `self.object` is available
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.save()
            return redirect(reverse("products:product-detail", kwargs={"pk": self.object.pk}))

        return self.render_to_response(self.get_context_data(form=form))
    

class AddToCartView(LoginRequiredMixin, View):
    """
    Handles adding a product to the cart.
    """

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = request.POST.get('quantity', 1)
        
        # Get or create a cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create a cart item for the specific product
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += int(quantity)
        cart_item.save()
        messages.success(self.request, f"Item '{cart_item.product.name}' Added to cart")

        return redirect(reverse("products:product-detail", kwargs={"pk": product.pk}))
    


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Handles adding a product to the cart.
    """
    def get(self, request, product_id):
        cart_item = get_object_or_404(CartItem, id=product_id)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(self.request, f"Item '{product_name}' Removed from cart")
        return redirect(reverse("products:cart-detail"))
    

class CartDetailView(TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        """Override to pass the cart for the logged-in user."""
        context = super().get_context_data(**kwargs)
        try:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart'] = cart
        except Cart.DoesNotExist:
            context['cart'] = None  # If no cart is found
        return context
    

class CheckoutView(TemplateView):
    template_name = "cart/checkout.html"

    def get_context_data(self, **kwargs):
        """Override to pass the cart for the logged-in user."""
        context = super().get_context_data(**kwargs)
        try:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
            context['cart'] = cart
        except Cart.DoesNotExist:
            context['cart'] = None  # If no cart is found
        return context
    
    
class ProductSearchView(View):

    def post(self, request):
        search = request.POST.get('search', None)
        if search:
            return redirect(reverse("products:product-list") + f"?search={search}")
        return redirect(reverse("products:product-list"))