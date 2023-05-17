from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework.settings import api_settings
from .models import Profiles

User = get_user_model() 

        
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Profiles
        fields = '__all__'
        
    def get_user(self, obj):
        # Access the user from the context or request
        # You can modify this logic based on your requirements
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user
        return None


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        
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
    
        
    def create(self, validated_data):
        profile_data = validated_data.get('profile')
        print("this is profile data" + str(profile_data))
              
        print("this is validated data" + str(validated_data))
        user = User.objects.create_user(
            validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save() 
        

        print('this is created user: ' + str(user))
        print("this is popped profile data: " + str(profile_data))
        profile = Profiles.objects.create(user=user,  **profile_data)
        
        print("created profile : " + str(profile))
        
        validated_data['profile'] = profile_data
        
        print("this is profile: " + str(profile))
        print("this is profile.user: " + str(profile.user))
        print("this is profile.user.id: " + str(profile.user.id))
        print("this is profile.name: " + str(profile.name))
        
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        print("this is data: " + str(data))
        return data