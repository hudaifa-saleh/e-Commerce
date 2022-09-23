from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from ecommerce.views import about_page, contact_page, login_page, register_page, home_page

urlpatterns = [
    re_path(r"^$", home_page, name="home"),
    re_path(r"^about/$", about_page, name="about"),
    re_path(r"^contact/$", contact_page, name="contact"),
    re_path(r"^login/$", login_page),
    re_path(r"^register/$", register_page),
    re_path(r"^cart/", include("carts.urls", namespace="cart")),
    re_path(r"^products/", include("products.urls", namespace="products")),
    re_path(r"^search/", include("search.urls", namespace="search")),
    re_path(r"^admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
