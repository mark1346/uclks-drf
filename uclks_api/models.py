# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone

### department_module
class DepartmentModule(models.Model):
    department = models.ForeignKey('Departments', models.DO_NOTHING)
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    study_year = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'department_module'
        unique_together = (('department', 'module'),)

### departments
class Departments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'departments'


###modules
class Modules(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'modules'


###feedback
class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    module = models.ForeignKey('Modules', related_name='feedbacks', on_delete=models.DO_NOTHING)
    
    COMPULSORY_CHOICES = (
        (0, 'Not Compulsory'),
        (1, 'Compulsory')
    )
    is_compulsory = models.IntegerField(choices=COMPULSORY_CHOICES, default=1)
    
    DIFFICULTY_CHOICES = (
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Normal'),
        (4, 'Difficult'),
        (5, 'Very Difficult'),
    )
    module_difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=3)
    
    ASSIGNMENT_AMOUNT_CHOICES = (
        (1, 'Very Few'),
        (2, 'Few'),
        (3, 'Normal'),
        (4, 'Many'),
        (5, 'Very Many')
    )
    amount_of_assignments = models.IntegerField(choices=ASSIGNMENT_AMOUNT_CHOICES, default=3)
    
    EXAM_DIFFICULTY_CHOICES = (
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Normal'),
        (4, 'Difficult'),
        (5, 'Very Difficult'),
    )
    exam_difficulty = models.IntegerField(choices=EXAM_DIFFICULTY_CHOICES, default=3)
    
    tips = models.TextField(blank=True, null=True)
    
    EVALUATION_CHOICES = (
        (1, 'Very Very Shxt'),
        (2, 'Very Shxt'),
        (3, 'Shit'),
        (4, 'Below Average'),
        (5, 'Average'),
        (6, 'Good'),
        (7, 'Very Good'),
        (8, 'Excellent'),
        (9, 'Fxcking Amazing'),
        (10, 'Free First'),
    )
    evaluation = models.IntegerField(choices=EVALUATION_CHOICES, default=5)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'feedback'



# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#     id = models.AutoField(primary_key=True)

#     class Meta:

#         db_table = 'auth_group'

# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)




# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         db_table = 'django_session'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        db_table = 'failed_jobs'



class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        db_table = 'migrations'



class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'password_resets'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'personal_access_tokens'

