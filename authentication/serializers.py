from rest_framework import serializers
from authentication.models import Registration
from django.conf import settings

from uuid import uuid4
import sys

def email_validators(email):
    email = email.strip()
    parts = email.split('@', 1)
    if len(parts) < 2:
        raise serializers.ValidationError('The email format is not valid')
    else:
        domain = parts[1]
        if domain not in settings.ALLOWED_DOMAINS:
            raise serializers.ValidationError('The email domain is not valid')

class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[email_validators])

    class Meta:
        model = Registration
        fields = ('email', 'active')
        read_only_fields = ('active',)

    def create(self, validated_data):
        email = validated_data['email']
        token = uuid4().hex
        registration, created = Registration.objects.update_or_create(
            email=email, 
            defaults={'email': email, 'token': token})
        return registration

