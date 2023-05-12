import uuid

from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm


def paypal(request, pk):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-ybtg722348950@business.example.com",
        "amount": "1.00",
        "item_name": "name of the item",
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('paypal_reverse')),
        "cancel_return": request.build_absolute_uri(reverse('paypal_cancel')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)



def paypal_reverse(request):
    messages.success(request, 'Success')
    return redirect('home')


def paypal_cancel(request):
    messages.error(request, 'Cancel')

    return redirect('home')
