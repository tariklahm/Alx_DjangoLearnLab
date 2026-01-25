from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create Book model.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()




class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, date_of_birth=None, profile_photo=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        if not username:
            raise ValueError("Username must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, date_of_birth=date_of_birth, profile_photo=profile_photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, username, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
