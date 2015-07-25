__author__ = 'dheerendra'

from gcm.models import get_device_model
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

def send_android_push_notification(message):
    Device = get_device_model()
    Device.objects.all().filter(is_active=True).send_message(message)

def verify_image(image):
    try:
        Image.open(image)
        return True
    except:
        return False
