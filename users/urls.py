from django.urls import path
from .views import UserRegisterAPIView, UserLoginAPIView, UserRetrieveAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'), # 회원가입
    path('login/', UserLoginAPIView.as_view(), name='login'), # 로그인
    path('auth/', UserRetrieveAPIView.as_view(), name='auth'), # 유저 정보
]
