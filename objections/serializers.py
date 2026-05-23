from rest_framework import serializers
from .models import Objection


class ObjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objection
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'processed_at']