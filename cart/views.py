from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, Order, OrderItem, Payment
import razorpay


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart_view')

    total = sum(item.total_price() for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        payment_method='razorpay',
        status='pending'
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    return render(request, 'cart/checkout.html', {
        'order': order,
        'total': total
    })


@login_required
def pay_now(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    razorpay_order = client.order.create({
        "amount": int(order.total_amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment.objects.create(
        order=order,
        razorpay_order_id=razorpay_order['id']
    )

    return render(request, 'cart/pay_now.html', {
        'order': order,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.paid = True
        payment.save()

        order = payment.order
        order.status = 'paid'
        order.save()

        Cart.objects.filter(user=order.user).delete()

        return redirect('my_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cart/my_orders.html', {'orders': orders})





@login_required
def increase_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart_view')


@login_required
def decrease_qty(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart_view')


@login_required
def remove_item(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart_view')
