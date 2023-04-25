from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings


### profiles
class Profiles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
    name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = (
        (0, 'Not Choosen'),
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)
    
    DEGREE_CHOICES = (
        (0, 'Not Choosen'),
        (1, 'Bachelor Degree'),
        (2, 'Master Degree'),
        (3, 'Graduated'),
    )
    degree = models.IntegerField(choices=DEGREE_CHOICES)
    
    department = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profiles'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

### users
class Users(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    role = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    #when logging in
    USERNAME_FIELD = 'email'
    
    #when creating superuser
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    class Meta:
        db_table = 'users'