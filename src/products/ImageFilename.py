import os
import random

from ecommerce.utils import unique_slug_generator


def get_filename_extension(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename, **kwargs):
    print(instance)
    print(filename)
    newFilename = random.randint(1, 3910209312)
    name, ext = get_filename_extension(filename)
    finalFilename = "{newFilename}{ext}".format(newFilename=newFilename, ext=ext)
    return "products/{newFilename}/{finalFilename}".format(newFilename=newFilename, finalFilename=finalFilename)


def upload_product_file_location(instance, filename):
    slug = instance.products.slug
    # id_ = 0
    id_ = instance.id
    print(instance.id)
    if id_ is None:
        klass = instance.__class__
        qs = klass.objects.all().order_by("-pk")
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.products)
    location = "product/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename
