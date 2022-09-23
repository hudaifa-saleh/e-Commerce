from django.urls import path, re_path
from carts.views import cart_home, cart_update

app_name = "carts"
urlpatterns = [
    re_path(r"^$", cart_home, name="home"),
    re_path(r"^update/$", cart_update, name="update"),
]
