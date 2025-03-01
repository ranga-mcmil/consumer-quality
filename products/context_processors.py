


from accounts.forms import CustomAuthenticationForm, RegistrationForm
from products.forms import ProductSearchForm
from products.models import Cart, Category


def base_data(request):

    data = {}
    data["categories"] = Category.objects.all()
    data["login_form"] = CustomAuthenticationForm()
    data["registration_form"] = RegistrationForm()
    data["search_form"] = ProductSearchForm()

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        data["cart_items"] = cart.total_quantity()
    else:
        data["cart_items"] = 0

    return data

