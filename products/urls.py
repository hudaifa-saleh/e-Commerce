from django.urls import path, re_path
from products.views import ProductDetailSlugView, ProductListView

app_name = "products"
urlpatterns = [
    re_path(r"^$", ProductListView.as_view(), name='list'),
    re_path(r"^(?P<slug>[\w-]+)/$", ProductDetailSlugView.as_view(), name="detail"),
]
