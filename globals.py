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

notice_priority = [('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Urgent')]

datetime_input_formats = [
     '%d-%m-%Y %H:%M',
]


def verify_image(image):
    try:
        Image.open(image)
        return True
    except:
        return False
