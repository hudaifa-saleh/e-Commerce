from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.conf import settings

# from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from django.core.files.storage import FileSystemStorage
from ecommerce.utils import get_filename, unique_slug_generator
from products.ImageFilename import upload_image_path, upload_product_file_location


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(price__icontains=query) | 
            Q(tag__title__icontains=query))
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class ProductModelManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Product.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False)

    objects = ProductModelManager()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs


####################################################### Signals ################################################################
def product_per_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_per_save_receiver, sender=Product)


class ProductFile(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    file = models.FileField(upload_to=upload_product_file_location, storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    free = models.BooleanField(default=False)  # purchase required
    user_required = models.BooleanField(default=False)  # user doesn't matter

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def get_download_url(self):  # detail view
        return reverse("products:download", kwargs={"slug": self.products.slug, "pk": self.pk})

    def get_default_url(self):
        return self.products.get_absolute_url()
