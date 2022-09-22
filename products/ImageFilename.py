import os
import random


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
