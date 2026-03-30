from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TodoList, TodoImage, userProfile

# Create your models here.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ['id', 'user', 'title', 'description', 'completed', 'created_at', 'updated_at']

class TodoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoImage
        fields = ['id', 'todo_list', 'image', 'uploaded_at', 'updated_at']

class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userProfile
        fields = ['user', 'profile_picture', 'bio', 'created_at', 'updated_at']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)  