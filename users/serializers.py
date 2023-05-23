from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.settings import api_settings
from .models import Profiles, Users

User = get_user_model() 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        exclude = ['user']
        
class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False) #이건 그냥 profile을 Meta에 사용하겠다. 라는 뜻이다.
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password],
        )
    
    class Meta:
        model = Users
        fields = ['id', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        profile_serializer = ProfileSerializer(data=profile_data) #이게 실제 profile data를 받아서 serializer를 만드는 과정이다.
        if profile_serializer.is_valid():
            profile = profile_serializer.save(user=user)
            user.profile = profile
        else:
            raise ValidationError(profile_serializer.errors)
        
        user.save()
        return user
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = Users
        fields = '__all__'
        