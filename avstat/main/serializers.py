from rest_framework import serializers
from .models import User, Stat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class UserStatSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="created_at")
    count = serializers.IntegerField(source="added")

    class Meta:
        model = Stat
        fields = ['date', 'count']
