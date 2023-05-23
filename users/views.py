from .serializers import UserRegisterSerializer, ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from .models import Profiles
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404

User = get_user_model()

class UserRegisterAPIView(APIView):
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
    # permission_classes=[isAuthenticated]
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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
            res = Response(user_serializer.data, status=status.HTTP_200_OK)
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        
        except jwt.exceptions.InvalidTokenError:
            # Invalid Token
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    