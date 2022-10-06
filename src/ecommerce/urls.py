from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LogoutView
from ecommerce.views import about_page, contact_page, home_page
from accounts.views import login_page, register_page, guest_register_view
from address.views import checkout_address_create_view

urlpatterns = [
    re_path(r"^$", home_page, name="home"),
    re_path(r"^about/$", about_page, name="about"),
    re_path(r"^contact/$", contact_page, name="contact"),
    re_path(r"^login/$", login_page, name="login"),
    re_path(r"^logout/$", LogoutView.as_view(), name="logout"),
    re_path(r"^register/$", register_page, name="register"),
    re_path(r"^register/guest/$", guest_register_view, name="guest_register"),
    re_path(r"^checkout/address/create/$", checkout_address_create_view, name="checkout_address_create"),
    re_path(r"^cart/", include("carts.urls", namespace="cart")),
    re_path(r"^products/", include("products.urls", namespace="products")),
    # re_path(r"^orders/", include("orders.urls", namespace="orders")),
    re_path(r"^search/", include("search.urls", namespace="search")),
    re_path(r"^admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
