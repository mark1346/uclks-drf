from .serializers import UserRegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

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
        serializer = UserRegisterSerializer(data=data)
        print(data)
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({'message': 'User created successfully'}, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)
    