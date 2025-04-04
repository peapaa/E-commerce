import os
from uuid import uuid4

def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid4().hex}.{ext}'
    return os.path.join('product', filename)