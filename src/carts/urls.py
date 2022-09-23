from django.urls import path, re_path
from carts.views import cart_home

app_name = "carts"
urlpatterns = [
    re_path(r"^$", cart_home, name="cart"),
]
