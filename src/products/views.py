import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.http import Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from library.models import LibraryPurchase
from products.models import Product, ProductFile
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin


class ProductFeaturedListView(LoginRequiredMixin, generic.ListView):
    template_name = "products/product_list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin, generic.DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featuerd_detail.html"


class ProductListView(generic.ListView):
    template_name = "products/product_list.html"
    success_url = "/list/"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, generic.DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        # object_viewed_signal.save(instance.__clean__, instance=instance, request=request)
        return instance


class ProductDetailView(ObjectViewedMixin, generic.DetailView):
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get("pk")
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance


class ProductPurchase:
    pass


class ProductDownloadView(generic.View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, products__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404('Download Not found')
        downloads_obj = downloads_qs.first()
        # Permission Checks
        can_download = False
        user_ready = True
        if downloads_obj.user_required:
            if request.user.is_authenticated:
                user_ready = False
        purchased_products = Product.objects.none()
        if downloads_obj.free:
            can_download = True
        else:
            # not free
            purchased_products = LibraryPurchase.objects.products_by_request(request)
            if downloads_obj.products in purchased_products:
                can_download = True
        if not can_download or not user_ready:
            messages.error(request, "You do not have access to download this item")
            return redirect(downloads_obj.get_default_url())

        file_root = settings.PROTECTED_ROOT
        file_path = downloads_obj.file.path
        final_file_path = os.path.join(file_root, file_path)
        with open(final_file_path, 'rb') as f:
            wrapper = FileWrapper(f)
            # content = 'some_text'
            mimetypes = 'application/force-download'
            guess_mimetypes = guess_type(file_path)[0] #file_name.MP4
            if guess_mimetypes:
                mimetypes = guess_mimetypes
            resource = HttpResponse(wrapper, content_type=mimetypes)
            resource['Content-Disposition'] = 'attachment;filename=%s '%(downloads_obj.display_name)
            resource['X-SendFile'] = str(downloads_obj.display_name)
            return resource
        # return redirect(download_obj.get_default_url())


