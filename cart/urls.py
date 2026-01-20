from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart_view'),

    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:id>/', views.remove_item, name='remove_item'),

    path('checkout/', views.checkout, name='checkout'),
    path('pay-now/<int:order_id>/', views.pay_now, name='pay_now'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
