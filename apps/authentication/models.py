from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)

def UserImages(instance, filename):
    return '/'.join( ['images', 'Users', str(instance.id), filename] )

class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=50, blank=True)
    cnic = models.CharField(max_length=13, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    DOB = models.DateField(default='2000-01-01')
    cell_contact = models.CharField(max_length=20)
    address = models.TextField()
    job_title = models.CharField(max_length=50)
    salary = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=UserImages, default='/images/Users/None/index.png')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username
