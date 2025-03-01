from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from paynow import Paynow
import time
from django.conf import settings
from django.core.mail import send_mail

from products.models import Cart


paynow = Paynow(
    '18546', 
    'dfb5b164-0f03-4b43-b553-0ddc9803da2a',
    'http://example.com/gateways/paynow/update', 
    'http://example.com/return?gateway=paynow'
)

class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # This method runs before the view is called for each request
        data_key = request.session.get('data_key', None)

        if data_key:
            poll_url = data_key['poll_url']
    
            # request.session.pop('data_key', None)

            i = 0
            while i < 5:
                status = paynow.check_transaction_status(poll_url)

                if status.status == 'paid':
                    cart = Cart.objects.get(user=request.user)
                    cart.items.all().delete()

                    self.complete_payment(request, "Payment Transaction SuccessFul")
                    messages.success(request, "Payment Transaction SuccessFul")
                    request.session.pop('data_key', None)
                    break

                if status.status == 'created': # Must have not been attended to
                    self.complete_payment(request, "Payment Transaction Failed")
                    request.session.pop('data_key', None)
                    messages.error(request, "Payment Transaction Failed")
                    
                    break   

                if status.status == 'cancelled':
                    self.complete_payment(request, "Payment Transaction Cancelled")
                    request.session.pop('data_key', None)
                    messages.warning(request, "Payment Transaction Cancelled")
                    break                
                time.sleep(1)
                i += 1      

    def complete_payment(self, request, message):

        send_mail(
            subject=f"Product Purchase",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )
