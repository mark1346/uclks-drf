from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Department, Module
from .serializers import (DepartmentSerializer, ModuleSerializer, UserSerializer,
                          UserChangePasswordSerializer, UserChangeEmailSerializer,
                          UserProfileSerializer, UserUpdateProfileSerializer)





class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.AllowAny,)


class DepartmentSearchView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        query = self.request.query_params.get("query")
        if query:
            return Department.objects.filter(name__icontains=query)
        return Department.objects.none()


class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (permissions.AllowAny,)


class ModuleDetailView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (permissions.AllowAny,)


class ModuleAverageView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, id):
        module = get_object_or_404(Module, id=id)
        average = module.get_average_score()
        return Response({"average": average}, status=status.HTTP_200_OK)


class UserInfoView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserProfileView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
