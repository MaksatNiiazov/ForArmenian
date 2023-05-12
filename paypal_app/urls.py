from django.urls import path
from paypal_app.views import paypal, paypal_reverse, paypal_cancel

urlpatterns = [
    path('paypal', paypal, name='home'),
    path('paypal_cancel', paypal_cancel, name='paypal_cancel'),
    path('paypal_reverse', paypal_reverse, name='paypal_reverse'),

]
