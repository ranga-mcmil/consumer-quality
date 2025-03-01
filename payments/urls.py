from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path("new/", views.NewPaymentView.as_view(), name="new_payment"),
]