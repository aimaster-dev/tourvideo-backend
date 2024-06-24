from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, username, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff = True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser = True.")
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    user_type = models.IntegerField(default=3)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    street = models.CharField(max_length=50, required = False)
    country = models.CharField(max_length=50, required = False)
    city = models.CharField(max_length=50, required = False)
    zipcode = models.CharField(max_length=20, required = False)
    state = models.CharField(max_length=50, required = False)
    get_same_video = models.BooleanField(default=True)
    appears_in_others_video = models.BooleanField(default=True)
    voice_can_be_recorded = models.BooleanField(default=True)
    be_shown_potential = models.BooleanField(default=True)
    be_shown_public_business = models.BooleanField(default=True)
    be_shown_social_media = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user_tbl'

    def __str__(self):
        return self.email