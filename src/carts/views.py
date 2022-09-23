from tkinter.messagebox import NO
from django.shortcuts import render
from carts.models import Cart, CartManager


def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {})
