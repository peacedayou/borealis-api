from rest_framework import serializers
from .models import BorealisDataset

class BorealisDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorealisDataset
        fields = '__all__'
