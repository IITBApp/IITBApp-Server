__author__ = 'dheerendra'

import django.dispatch

feed_entry_registered = django.dispatch.Signal(providing_args=['instance, created'])
