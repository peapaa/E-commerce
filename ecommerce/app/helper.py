import os
from uuid import uuid4

def create_product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('product', filename)