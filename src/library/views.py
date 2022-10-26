from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from library.models import LibraryPurchase


class LibraryView(LoginRequiredMixin, ListView):
    template_name = "library/library.html"

    def get_queryset(self):
        return LibraryPurchase.objects.by_request(self.request).digital()
