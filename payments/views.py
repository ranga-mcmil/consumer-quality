from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from payments.ecocash import make_payment

# Create your views here.
class NewPaymentView(View):
    def get(self, request, *args, **kwargs):
        try:
            redirect_url, poll_url = make_payment(f'Order ', request.user.email, 1)
            request.session['data_key'] = {"poll_url": poll_url}
            return HttpResponseRedirect(redirect_url, status=302)
        except:
            messages.error(request, 'Something happened, make sure you are connected to the internet to complete Ecocash payment')
            return redirect(request.META['HTTP_REFERER'])