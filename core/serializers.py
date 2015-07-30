__author__ = 'dheerendra'


from rest_framework import serializers
from models import BugTracker


class BugTrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BugTracker