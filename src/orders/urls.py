from django.urls import path, re_path
from orders.views import OrderListView, OrderDetailView

app_name = "products"
urlpatterns = [
    re_path(r"^$", OrderListView.as_view(), name='list'),
    re_path(r"^(?P<order_id>[0-9A-Za-z]+)$", OrderDetailView.as_view(), name="detail"),
]
