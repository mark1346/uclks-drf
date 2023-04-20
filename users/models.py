from django.db import models

# Create your models here.

### profiles
class Profiles(models.Model):
    user = models.OneToOneField('Users', models.CASCADE)
    name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField()
    degree = models.IntegerField()
    department = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'profiles'

### users
class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    role = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'