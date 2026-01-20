from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth (login/logout)
    path('accounts/', include('django.contrib.auth.urls')),

    # custom accounts
    path('accounts/', include('accounts.urls')),
    
    path('', include('products.urls')),
    #path('', include('cart.urls')),
     path('cart/', include('cart.urls')),

]






