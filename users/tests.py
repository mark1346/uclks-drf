from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import date

from users.serializers import UserRegisterSerializer, ProfileSerializer
from users.models import Profiles

User = get_user_model()

class UserLoginAPIViewTestCase(APITestCase):
    maxDiff = None
    def setUp(self):
        self.valid_data = {
            'email': 'logintest@gmail.com',
            'password': '6gkrsus7qks',
            'profile': {
                'name': 'Login Tester',
            }
        }
        self.client = APIClient()
        self.login_url = reverse('login')
        
    def test_user_login(self):
        serializer = UserRegisterSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profiles.objects.get(user=user)
        
        # the request data
        data = {
            'email': 'logintest@gmail.com',
            'password': '6gkrsus7qks',
            'profile': {
                'name': 'Login Tester',
            }
        }
        
        # Make API call to login user
        response = self.client.post(self.login_url, data, format='json')
        
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print("this is response data:" + str(response.data))
        
        # Assert the response data
        expected_data = {
            'user': {
                'id': 1,
                'email': 'logintest@gmail.com',
                'profile': {
                    'id': response.data['user']['profile']['id'],
                    'name': 'Login Tester',
                    'birthday': None,
                    'gender': 0,
                    'degree': 0,
                    'department': None,
                    'created_at': response.data['user']['profile']['created_at'],
                    'updated_at': response.data['user']['profile']['updated_at'],
                },
                    
            },
            'message': 'User logged in successfully',
            'token': {
                'access_token': str(response.data['token']['access_token']),
                'refresh_token': str(response.data['token']['refresh_token']),
            }
        }
        self.assertEqual(response.data, expected_data)
        
        
            

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

        self.user_data = {
            'email': 'john13doe@example.com',
            'password': '6gkrsus7qks',
            'name': 'John Doe',
        }
        
        # self.invalid_user_data = {
        #     'email': 'invalidemail',
        #     'password': '6gkrsus7qks',
        #     'profile': {
        #         'name': 'John Doe',
        #     }
        # }

    # def test_user_registration(self):
    #     response = self.client.post(self.register_url, self.user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(get_user_model().objects.count(), 1)
    #     self.assertEqual(Profiles.objects.count(), 1)
    #     self.assertEqual(get_user_model().objects.get().email, self.user_data['email'])

    # def test_invalid_user_registration(self):
    #     response = self.client.post(self.register_url, self.invalid_user_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class UserRegisterSerializerTest(TestCase):
#     def setUp(self):
#         self.valid_data = {
#             'email': 'johndoe@example.com',
#             'password': '6gkrsus7qks',
#             'profile': {
#                 'name': 'John Doe',
#             }
#         }
    
#     def test_create_user_and_profile(self):
#         print(self.valid_data)
#         serializer = UserRegisterSerializer(data=self.valid_data)
#         serializer.is_valid(raise_exception=True)
#         print("this is error:" + str(serializer.errors))
        
#         user = serializer.save()
        
#         # Check that a user and profile were created with the correct data
#         self.assertEqual(user.email, self.valid_data['email'])
#         self.assertTrue(user.check_password(self.valid_data['password']))
#         profile = Profiles.objects.get(user=user)
#         self.assertEqual(profile.name, self.valid_data['profile']['name'])
#         self.assertEqual(profile.gender, 0)
#         self.assertEqual(profile.degree, 0)
    
#     def test_password_validation(self):
#         self.valid_data['password'] = 'asd'
#         serializer = UserRegisterSerializer(data=self.valid_data)
#         serializer.is_valid()
#         print("this is error:" + str(serializer.errors))
#         # self.assertEqual(serializer.errors['password'][0], 
#         #                  serializers.Field.default_error_messages['min_length'].format(8))
    
#     def test_email_uniqueness(self):
#         User.objects.create_user(email=self.valid_data['email'], password=self.valid_data['password'])
#         serializer = UserRegisterSerializer(data=self.valid_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertEqual(serializer.errors['email'][0], 'This field must be unique.')
