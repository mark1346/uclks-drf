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
        
        
        
#   class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Profiles
#         fields = '__all__'
        
#     def get_user(self, obj):
#         # Access the user from the context or request
#         # You can modify this logic based on your requirements
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             return request.user
#         return None


# class UserRegisterSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer(required=False)
    
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'profile')
        
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())],
    #     )
    # password = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     style={'input_type': 'password'},
    #     validators=[validate_password],
    #     )
    
        
#     def create(self, validated_data):
#         profile_data = validated_data.get('profile')
#         print("this is profile data" + str(profile_data))
              
#         print("this is validated data" + str(validated_data))
#         user = User.objects.create_user(
#             validated_data['email'],
#         )
#         user.set_password(validated_data['password'])
#         user.save() 
        

#         print('this is created user: ' + str(user))
#         print("this is popped profile data: " + str(profile_data))
        
#         created_profile = Profiles.objects.create(user=user,  **profile_data)
        
#         print("created profile : " + str(created_profile))
#         print("this is profile: " + str(created_profile))
#         print("this is profile.user: " + str(created_profile.user))
#         print("this is profile.user.id: " + str(created_profile.user.id))
#         print("this is profile.name: " + str(created_profile.name))
        
#         validated_data['profile'] = created_profile
#         print("this is validated data after profile: " + str(validated_data))
#         print("this is serialzier.data: " + str(self.data))
#         return user
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     print("this is data: " + str(data))
    #     return data