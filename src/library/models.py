from django.db import models
from billing.models import BillingProfile
from products.models import Product


class LibraryPurchaseQuerSet(models.query.QuerySet):
    def by_request(self, request, *args, **kwargs):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def active(self):
        return self.filter(refunded=False)

    def digital(self):
        return self.filter(product__is_digital=True)


class LibraryPurchaseManager(models.Manager):
    def get_queryset(self):
        return LibraryPurchaseQuerSet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        return self.get_queryset().active().digital()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_id(self, request):
        qs = self.by_request(request).digital()
        ids_ = [x.product.id for x in qs]
        return ids_

    def products_by_request(self, request):
        ids_ = self.products_by_id(request)
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs


class LibraryPurchase(models.Model):
    # user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120)
    billing_profile = models.ForeignKey(BillingProfile, blank=True, null=True, on_delete=models.CASCADE)  # billingprofile.productpurchases_set.all()
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)  # product.productpurchases_set.all().count()
    refunded = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = LibraryPurchaseManager()

    def __str__(self):
        return self.product.title
