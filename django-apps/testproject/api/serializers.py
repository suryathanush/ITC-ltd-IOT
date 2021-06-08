from django.db.models import fields
from rest_framework import serializers
from .models import RegisterValuesEm6400


class ddbserialize(serializers.ModelSerializer):
    class Meta:
        model = RegisterValuesEm6400
        fields = "__all__"
