from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.api.serializers import CustomUserSerializer, LoginSerializer
from user.models import CustomUser


class CustomUserCreate(generics.CreateAPIView):
    model = CustomUser
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            # messages.success(request, 'Your account has been successfully registered. Please login to continue'))
            return Response({'Your account has been successfully registered. Please login to continue'})

    def perform_create(self, serializer):

        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class CustomUserLogin(generics.CreateAPIView):
    model = CustomUser
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            if request.data['next']:
                return HttpResponseRedirect(redirect_to=request.data['next'])
            return redirect('core:index')
        else:
            return Response({'serializer': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        if isinstance(self.request.user, AnonymousUser):
            return Response({'error': 'just logged in user can log out'}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return redirect('core:index')
