from django.urls import path, re_path
from library.views import LibraryView


app_name = "library"
urlpatterns = [
    re_path(r"^$", LibraryView.as_view(), name="library"),
]
