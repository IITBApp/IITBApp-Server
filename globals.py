__author__ = 'dheerendra'

from django.db import models
from PIL import Image

categories = [
    ('music', 'Music'),
    ('photo', 'Photography'),
    ('art', 'Fine Arts'),
    ('sports', 'Sports'),
    ('activity', 'Activity'),
    ('tech', 'Tech'),
    ('food', 'Food'),
    ('literature', 'Literature'),
]

def verify_image(image):
    try:
        Image.open(image)
        return True
    except:
        return False