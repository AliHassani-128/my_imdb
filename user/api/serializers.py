from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from user.models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True, style={'placeholder': 'Username'})
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password],
                                     style={'input_type': 'password', 'placeholder': 'Password'})
    password_again = serializers.CharField(write_only=True, required=True,
                                           style={'input_type': 'password', 'placeholder': 'Password Again'})
    email = serializers.CharField(write_only=True, required=True, style={'placeholder': 'Email'})

    class Meta:
        model = CustomUser
        depth = 1
        fields = ['username','first_name','last_name','password','password_again','email']

    def create(self, validated_data):

        customuser = CustomUser.objects.create(username=validated_data['username'],
                                           first_name=validated_data['first_name'],
                                           last_name=validated_data['last_name'],
                                           password=make_password(validated_data['password']),
                                           email=validated_data['email'],
                                           )


        return customuser

    def validate(self, attrs):
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "This username is used!"})
        if attrs['password'] != attrs['password_again']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs['email']:
            raise serializers.ValidationError({'emil': 'Email field is required'})
        return attrs

    def validate_username(self, username):
        if len(username) < 4 or len(username) > 15:
            raise ValidationError('Username must be between 4 and 15 characters long')
        return username


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, style={'placeholder': 'Username'})

    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    def validate(self, attrs):
        if attrs['username'] and attrs['password']:
            try:
                CustomUser.objects.get(username=attrs['username'])
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('CustomUser with this username does not exists please sign up first!')
            user = authenticate(username=attrs['username'], password=attrs['password'])
        else:
            raise serializers.ValidationError('Username and password are required')
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}

