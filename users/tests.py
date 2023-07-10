from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import datetime, timedelta

from users.serializers import UserRegisterSerializer, ProfileSerializer, UserSerializer
from users.models import Profiles

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt
from django.conf import settings
from django.core import mail
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from django.utils import timezone
from django.core.mail import send_mail

User = get_user_model()

class SendVerificationEmailAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='markymark331@gmail.com', password='testpassword')
        self.client = APIClient()
        self.url = reverse('send-email-verification')
    
    def test_real_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        # send_mail(
        #     subject='Email Verification',
        #     message=f'Click the link to verify your email: ',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[self.user.email],
        #     fail_silently=False,
        # )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Verification email sent.')
        
    # def test_send_verification_email(self):
    #     self.client.force_authenticate(user=self.user)
        
    #     # send a verification email
    #     response = self.client.post(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'Verification email sent.')
    
    #     # Verify that an email has been sent
    #     print("this is mail subject: " + mail.outbox[0].subject)
    #     print("this is mail body: " + mail.outbox[0].body)
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].subject, 'Email Verification from UCLKS Website')
    #     self.assertEqual(mail.outbox[0].to, [self.user.email])
    
# class HandleEmailVerificationAPITestCase(APITestCase):
#     def test_handle_email_verification(self):
#         # Create a user and an email address with an unverified status
#         self.user = User.objects.create_user(email='HVEtestemail', password='testpassword')
#         email_address = EmailAddress.objects.create(user=self.user, email=self.user.email, verified=False)
        
#         # Generate an email confirmation key
#         email_confirmation = EmailConfirmation.create(email_address)
#         email_confirmation.sent = timezone.now()
#         print("this is email_confirmation: " + str(email_confirmation))
#         email_confirmation.save()
#         key = email_confirmation.key
#         print("this is key in test: " + key)
        
        
#         # Perform email verification with the key
#         url = reverse('handle-email-verification', kwargs={'key': key})
#         response = self.client.post(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print("This is from HMAC:" + str(EmailConfirmationHMAC.from_key(key)))
#         print("this is EmailConfirmation.from_key: " + str(EmailConfirmation.objects.filter(key=key).first()))

        
#         # Verify that the email address has been verified and role is updated
#         email_address.refresh_from_db()
#         self.assertEqual(email_address.verified, True)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.role, 1)
        
        

       
# class ProfileUpdateAPITestCase(APITestCase):
#     def setUp(self):
#         # 유저 만들기
#         self.client = APIClient()
#         self.register_url = reverse('register')
#         self.user_data = {
#             'email': 'mark@example.com',
#             'password': '6gkrsus7qks',
#             'name': 'Mark Han',
#         }
#         self.register_response = self.client.post(self.register_url, self.user_data, format='json')
#         self.user_data = self.register_response.data['user']
#         # self.profile = self.user_data['profile']
#         self.update_url = reverse('profile-update')
        
#         self.user = User.objects.get(email=self.user_data['email'])
        
#     def test_update_profile_authenticated(self):
#         token = AccessToken.for_user(self.user)
#         headers = {'Authorization': f'Bearer {token}'}

#         self.client.force_authenticate(user=self.user)
#         print("this is response data: " + str(self.register_response.data))
#         updating_data = {
#             'name': 'Sunghyun Han',
#             'birthday': '1999-08-25',
#             'gender': 1,
#             'degree': 1,
#             'department': 'Computer Science',
#         }
        
#         response = self.client.post(self.update_url, updating_data, format='json', headers=headers)
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Profile updated successfully')
        
#         self.profile = Profiles.objects.get(user=self.user)
#         print("this is profile data: " + str(self.profile))
        
#         self.assertEqual(self.profile.name, updating_data['name'])
#         self.assertEqual(str(self.profile.birthday), updating_data['birthday'])
#         self.assertEqual(self.profile.gender, updating_data['gender'])
#         self.assertEqual(self.profile.degree, updating_data['degree'])
#         self.assertEqual(self.profile.department, updating_data['department'])


# class EmailChangeAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='emailchange@example.com', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('email-change')
    
#     def test_change_email(self):
#         new_email = 'newemail@example.com'
#         data = {'email': new_email}
        
#         response = self.client.post(self.url, data)
        
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Email changed successfully')
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.email, new_email)
    
    
# class PasswordChangeAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='pwchangetest@example.com', password='oldpassword')
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse('password-change')
    
#     def test_password_change(self):
#         data = {
#             'current-password': 'oldpassword',
#             'new-password': 'newpassword',
#             'confirmation': 'newpassword',
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'Password changed successfully.')
        
#         # Check that the user's password has changed
#         self.user.refresh_from_db()
#         self.assertTrue(self.user.check_password('newpassword'))
            
# class UserDeleteAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='deletetest@gmail.com', password='testpassword')
#         # self.access_token = AccessToken.for_user(self.user)
#         # self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.access_token)) # access token을 header에 넣어줌
#         self.delete_url = reverse('user-delete')
#         print("this is self.user:" + str(self.user))
    
#     def test_delete_user(self):
#         # Send a DELETE request to delete the user
#         self.client.force_authenticate(user=self.user)
#         response = self.client.delete(self.delete_url)
#         print("this is response:" + str(response))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        
#     def test_delete_user_unauthenticated(self):
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
            
# class UserUpdateAPITestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
#         self.client.force_authenticate(user=self.user)
#         self.update_url = reverse('user-update')

#     def test_update_user(self):
#         # Send a PUT request to update the user
#         data = {
#             'email': 'updatedemail@example.com',
#             'password': 'updatedpassword',
#             'profile': {
#                 'name': 'Updated Name'
#             }
#         }
#         response = self.client.put(self.update_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Add assertions to check the updated user data in the response
#         # For example: self.assertEqual(response.data['email'], 'updatedemail@example.com')

# class UserRetrieveAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(email='testuser', password='testpassword')
#         self.profile = Profiles.objects.create(user=self.user, name='testname')
#         print("this is user:" + str(self.user))
        
#         # Generate tokens
#         self.access_token = AccessToken.for_user(self.user)
#         self.refresh_token = RefreshToken.for_user(self.user)
        
#         # Set tokens in client's cookies
#         self.client.cookies['access_token'] = self.access_token
#         self.client.cookies['refresh_token'] = self.refresh_token
        
#         self.auth_url = reverse('auth')

#     def test_retrieve_user(self):
#         response = self.client.get(self.auth_url, format='json')
#         print("this is response:" + str(response))
#         print("this is response.data:" + str(response.data))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.user.id)
#         self.assertEqual(response.data['email'], self.user.email)


#     def test_retrieve_user_with_expired_access_token(self):
#         # Simulate an expired access token
#         expired_time = datetime.utcnow() - timedelta(minutes=65)
#         payload = {
#             'user_id': self.user.id,
#             'exp': expired_time
#         }
#         expired_access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#         self.client.cookies['access_token'] = expired_access_token
        
#         response = self.client.get(self.auth_url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.user.id)
#         self.assertEqual(response.data['email'], self.user.email)


#     def test_retrieve_user_with_invalid_access_token(self):
#         # Simulate an invalid access token
#         invalid_token = 'invalid_token_value'
        
#         self.client.cookies['access_token'] = invalid_token
        
#         response = self.client.get(self.auth_url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
# class UserLoginAPIViewTestCase(APITestCase):
#     maxDiff = None
#     def setUp(self):
#         self.valid_data = {
#             'email': 'logintest@gmail.com',
#             'password': '6gkrsus7qks',
#             'profile': {
#                 'name': 'Login Tester',
#             }
#         }
#         self.client = APIClient()
#         self.login_url = reverse('login')
        
#     def test_user_login(self):
#         serializer = UserRegisterSerializer(data=self.valid_data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         profile = Profiles.objects.get(user=user)
        
#         # the request data
#         data = {
#             'email': 'logintest@gmail.com',
#             'password': '6gkrsus7qks',
#             'profile': {
#                 'name': 'Login Tester',
#             }
#         }
        
#         # Make API call to login user
#         response = self.client.post(self.login_url, data, format='json')
        
#         # Assert the response status code
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         print("this is response data:" + str(response.data))
        
#         # Assert the response data
#         expected_data = {
#             'user': {
#                 'id': 1,
#                 'email': 'logintest@gmail.com',
#                 'profile': {
#                     'id': response.data['user']['profile']['id'],
#                     'name': 'Login Tester',
#                     'birthday': None,
#                     'gender': 0,
#                     'degree': 0,
#                     'department': None,
#                     'created_at': response.data['user']['profile']['created_at'],
#                     'updated_at': response.data['user']['profile']['updated_at'],
#                 },
                    
#             },
#             'message': 'User logged in successfully',
#             'token': {
#                 'access_token': str(response.data['token']['access_token']),
#                 'refresh_token': str(response.data['token']['refresh_token']),
#             }
#         }
#         self.assertEqual(response.data, expected_data)
        
        
            

# class UserRegistrationTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.register_url = reverse('register')

#         self.user_data = {
#             'email': 'john13doe@example.com',
#             'password': '6gkrsus7qks',
#             'name': 'John Doe',
#         }
        
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
