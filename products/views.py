from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from cart.models import Cart
from django.contrib.auth.decorators import login_required


def home(request):
    products = Product.objects.all()
    return render(request, "products/home.html", {"products": products})
    



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/detail.html", {"product": product})


#@login_required
#def add_to_cart(request, product_id):
 #   if request.method == "POST":
#        product = get_object_or_404(Product, id=product_id)
#
 #       cart_item, created = Cart.objects.get_or_create(
 #           user=request.user,
  #          product=product
   #     )
#
 #       if not created:
  #          cart_item.quantity += 1
   #         cart_item.save()
#
 #       return redirect("cart_view")
#
 #   return redirect("detail", id=product_id)








@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')
