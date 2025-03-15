from rest_framework import serializers
from ..models import Post, Job
from django.contrib.auth.models import User
from ..models import UserProfile

# class DeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post 
#         fields = ['id', 'title', 'status']


# serializers.py
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'user', 'company', 'place', 'status']






class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user',)