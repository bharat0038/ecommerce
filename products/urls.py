from django.urls import path
from .views import home, product_detail, add_to_cart

urlpatterns = [
    path('', home, name='home'),
   
    
    
    path('product/<int:id>/', product_detail, name='product_detail'),
    
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

]