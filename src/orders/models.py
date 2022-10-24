import math
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from address.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
)


class OrderManagerQuerySet(models.query.QuerySet):
    def by_request(self, request, *args, **kwargs):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self, request):
        return self.exclude(status="created")


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status="created",
        )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, related_name="billing_profile", blank=True, null=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name="billing_address", blank=True, null=True, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", blank=True, null=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="cart", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(max_length=120, default="created", choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = OrderManager()

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, ".2f")
        self.total = formatted_total
        self.save()
        return new_total

    def cheke_done(self):
        shipping_address_required = not self.cart.is_digital
        shipping_done = False

        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True

        # if not shipping_address_required and not self.shipping_address:
        #     shipping_done = True
        # if shipping_address_required and not self.shipping_address:
        #     shipping_done = False

        billing_profile = self.billing_profile
        billing_address = self.billing_address
        # shipping_address = self.shipping_address
        total = self.total
        if billing_profile and billing_address and shipping_done and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.cheke_done():
            self.status = "paid"
            self.save()
        return self.status

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"order_id": self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"


####################################################### Signals ################################################################
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    print("Running...")
    if created:
        print("Updating.... First")
        instance.update_total()


post_save.connect(post_save_order, sender=Order)
