from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password', 'username', 'id')
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)