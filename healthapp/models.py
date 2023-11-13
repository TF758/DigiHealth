from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Address(models.Model):
    DISTRICTS = [
        ("ALR", "Anse La Raye"),
        ("CAN", "Canaries"),
        ("CAS", "Castries"),
        ("CHO", "Choiseul"),
        ("DEN", "Dennery"),
        ("GI", "Gros Islet"),
        ("LAB", "Laborie"),
        ("MIC", "Micoud"),
        ("SOU", "Soufirere"),
        ("VF", "Vieux Fort"),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    address1 = models.CharField(
        "Address line 1",
        max_length=1024, null=True
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024, null=True
    )

    district = models.CharField(max_length=150, null=True, choices=DISTRICTS)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return str(self.user.first_name +" " + self.user.last_name+" " + self.district)

class UserProfile(models.Model):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=150, null=True, choices=GENDERS)
    
    def __str__(self):
        return  str(self.user.first_name +" " + self.user.last_name)
    
class Center (models.Model):
    DISTRICTS = [
        ("ALR", "Anse La Raye"),
        ("CAN", "Canaries"),
        ("CAS", "Castries"),
        ("CHO", "Choiseul"),
        ("DEN", "Dennery"),
        ("GI", "Gros Islet"),
        ("LAB", "Laborie"),
        ("MIC", "Micoud"),
        ("SOU", "Soufirere"),
        ("VF", "Vieux Fort"),
    ]
    name = models.CharField(max_length=150, null=True)
    center_abbreviation = models.CharField(max_length=20, null=True)
    district = models.CharField(max_length=150, null=True, choices=DISTRICTS)
    contact = models.CharField(max_length=150)
    center_image = models.ImageField(upload_to='center_images')

    def __str__(self):
        return self.center_abbreviation

class ClinicType (models.Model):

    type_name = models.CharField(max_length=150, null=True)
    type_abbreviation = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.type_abbreviation


class ClinicEvent(models.Model):
    STATUS = [
        ("urgent", "Urgent Care"),
        ("phc", "Primary Health Care"),
        ("other", "Other"),
    ]
    event_name = models.CharField(max_length=255, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=datetime.date.today, null=True)
    end_date = models.DateField(default=datetime.date.today, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    clinic_status = models.CharField(
        choices=STATUS, max_length=125, null=True)
    is_active = models.BooleanField(default=False, null=True)
    facility = models.ForeignKey(
        Center, null=True, on_delete=models.DO_NOTHING)
    clinic_type = models.ForeignKey(
        ClinicType, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.event_name)
    