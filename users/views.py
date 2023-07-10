from .serializers import UserRegisterSerializer, ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password
from .models import Profiles
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerOrReadOnly
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from django.utils import timezone
from allauth.account.utils import send_email_confirmation


User = get_user_model()

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'profile': {
                'name': request.data.get('name'),
            }
        }
        print("this is request data :" + str(request.data))
        print("this is data after parsing: " + str(data))
        serializer = UserRegisterSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            print("this is serializer data:" + str(serializer.data))
            
            #jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "User created successfully",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token
                    },
                },
                status=status.HTTP_201_CREATED
            )
            
            #jwt token을 cookie에 저장
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            
            return res
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    #로그인
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # User credentials are valid(이미 가입)-> generate JWT tokens
            # print("this is user from authenticate :" + str(user))
            serializer = UserRegisterSerializer(user, context={'request': request})
            
            tokens = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(tokens)
            access_token = str(tokens.access_token)
            
            profile = Profiles.objects.get(user=user)
            profile_data = ProfileSerializer(profile).data
            
            user_data = serializer.data
            user_data['profile'] = profile_data
            
            res = Response(
                {
                    "user": user_data,
                    "message": "User logged in successfully",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )   
            
            #jwt token을 cookie에 저장
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        else:
            return Response(
                {"detail": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserRetrieveAPIView(APIView):
    # permission_classes=[IsAuthenticated]
    serializer_class = UserSerializer
    
    #유저 정보 확인
    def get(self, request):
        try:
            # Access Token decoding and User Identification
            access = request.COOKIES.get('access_token')
            print("this is access token from cookie: " + str(access))
            payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            serializer = UserSerializer(instance=user)
            profile = Profiles.objects.get(user=user)
            profile_data = ProfileSerializer(profile).data
            
            user_data = serializer.data
            user_data['profile'] = profile_data
            
            return Response(user_data, status=status.HTTP_200_OK)
        
        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh_token')}
            token_serializer = TokenRefreshSerializer(data=data)
            token_serializer.is_valid(raise_exception=True)
            access_token = token_serializer.validated_data.get('access')
            refresh_token = token_serializer.validated_data.get('refresh')
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            user_serializer = UserSerializer(instance=user)
            
            profile = Profiles.objects.get(user=user)
            profile_data = ProfileSerializer(profile).data
            
            user_data = user_serializer.data
            user_data['profile'] = profile_data
            
            res = Response(user_data, status=status.HTTP_200_OK)
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        
        except jwt.exceptions.InvalidTokenError:
            # Invalid Token
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    
class UserUpdateAPIView(UpdateAPIView):
    permission_classes=[IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_object(self):
        return self.request.user
    
class UserDeleteAPIView(APIView):
    permission_classes=[IsAuthenticated, IsOwnerOrReadOnly]
    
    def delete(self, request):
        try:
            user = request.user
            user.delete()
            # print("this is user from request: " + str(user))
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordChangeAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    def post(self, request):
        user = request.user
        current_password = request.data.get('current-password')
        new_password = request.data.get('new-password')
        confirmation_password = request.data.get('confirmation')

        if not current_password or not new_password or not confirmation_password:
            return Response({'error': 'Please provide all the required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirmation_password:
            return Response({'error': 'New password and confirmation do not match.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(current_password, user.password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
class EmailChangeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    def post(self, request):
        try:
            email = request.data.get('email')
            
            # Get the current user
            user = request.user
            
            # Update the email
            user.email = email
            user.save()
            
            return Response({"message": "Email changed successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProfileUpdateAPIView(UpdateAPIView):
    permission_classes=[IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request):
        try:
            user = request.user
            profile = Profiles.objects.get(user=user)
            
            # parse the request data
            data = {
                'name': request.data.get('name'),
                'birthday': request.data.get('birthday'),
                'gender': request.data.get('gender'),
                'degree': request.data.get('degree'),
                'department': request.data.get('department'),
            }
            profile_serializer = ProfileSerializer(instance=profile, data=data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SendVerificationEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user  # Assuming the user is authenticated
        email = user.email
        
        # Create and save the EmailAddress instance if not already created
        email_address, _ = EmailAddress.objects.get_or_create(user=user, email=email)
        
        # Send the verification email
        email_confirmation = EmailConfirmation.create(email_address)
        send_email_confirmation(request, email_confirmation.email_address.user)
        email_confirmation.sent = timezone.now()
        email_confirmation.save()
        print("this is email_confirmation: " + str(email_confirmation))
        print("this is email_confirmation.key: " + str(email_confirmation.key))
        
        # Return the success message
        return Response({'message': 'Verification email sent.'})

class HandleEmailVerificationAPIView(APIView):
    def post(self, request, key):
        print("this is key in view: " + str(key))
        email_confirmation = EmailConfirmation.objects.filter(key=key).first()
        print("this is email_confirmation in view: " + str(email_confirmation))
        
        if email_confirmation is not None and email_confirmation.sent < timezone.now():
            # Email confirmation exists and is valid
            print("email confirmed")
            email_confirmation.confirm(request)
            print("email_confirmation.email_address.user: " + str(email_confirmation.email_address.verified))
            user = email_confirmation.email_address.user
            user.role = 1
            user.save()
            return Response({'message': 'Email verified successfully.'})
        else:
            return Response({'error': 'Invalid verification key.'}, status=status.HTTP_400_BAD_REQUEST)