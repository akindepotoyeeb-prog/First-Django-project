from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TodoList, TodoImage, userProfile
from .serializers import UserSerializer, TodoListSerializer, TodoImageSerializer, userProfileSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# generic views
from rest_framework import generics


# Create your views here.

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
   
class LoginUser(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutUser(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    
class UserProfile(generics.GenericAPIView):
    serializer_class = userProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = userProfile.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile, created = userProfile.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TodoListView(generics.GenericAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)

    def get(self, request):
        todo_list = self.get_queryset()
        serializer = self.serializer_class(todo_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        todo_list_id = request.data.get('id')
        try:
            todo_list = self.get_queryset().get(id=todo_list_id)
            serializer = self.serializer_class(todo_list, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TodoImageView(generics.GenericAPIView):
    serializer_class = TodoImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TodoImage.objects.filter(todo_list__user=self.request.user)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        todo_images = TodoImage.objects.filter(todo_list__user=request.user)
        serializer = self.serializer_class(todo_images, many=True)
        return Response(serializer.data)