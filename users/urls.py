from django.urls import path
from .views import (
    UserRegisterAPIView, 
    UserLoginAPIView, 
    UserRetrieveAPIView, 
    UserUpdateAPIView, 
    UserDeleteAPIView, 
    PasswordChangeAPIView, 
    EmailChangeAPIView,
    ProfileUpdateAPIView,
    SendVerificationEmailAPIView,
    HandleEmailVerificationAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='register'), # 회원가입
    path('login/', UserLoginAPIView.as_view(), name='login'), # 로그인
    path('auth/', UserRetrieveAPIView.as_view(), name='auth'), # 유저 정보
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'), # jwt 토큰 재발급
    path('update/', UserUpdateAPIView.as_view(), name='user-update'), # 유저 정보 수정
    path('delete/', UserDeleteAPIView.as_view(), name='user-delete'), # 유저 정보 삭제
    path('password/edit', PasswordChangeAPIView.as_view(), name='password-change'), # 비밀번호 변경
    path('email/edit', EmailChangeAPIView.as_view(), name='email-change'), # 이메일 변경
    path('profile/edit', ProfileUpdateAPIView.as_view(), name='profile-update'), # 프로필 변경
    path('send-email-verification', SendVerificationEmailAPIView().as_view(), name='send-email-verification'), # 이메일 인증 메일 보내기
    path('handle-email-verification/<str:key>', HandleEmailVerificationAPIView.as_view(), name='handle-email-verification'), # 이메일 인증 처리
    path('confirm-email/<str:key>', ConfirmEmailView.as_view(), name='account_confirm_email'), # all auth 이메일 인증
]
