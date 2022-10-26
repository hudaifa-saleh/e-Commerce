from django.http import Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order

# from django.shortcuts import render


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/order_list.html"

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created(self.request)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/order_detail.html"

    def get_object(self):
        qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get("order_id"))
        if qs.count() == 1:
            return qs.first()
        else:
            return Http404

    def get_queryset(self):
        return Order.objects.by_request(self.request)



