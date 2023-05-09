from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

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
        user = self.context['request'].user
        return user.id if user.is_authenticated else None


class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    
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
        print(validated_data)
        print("this is validated data")
        user = User.objects.create_user(
            validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save() 
        print('this is user before profile: ' + str(user))
        profile_data = validated_data.pop('profile')
        profile_data['user'] = user
        print('this is user: ' + str(user))
        Profiles.objects.create( **profile_data)
        
        return user