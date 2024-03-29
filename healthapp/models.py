from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
from taggit.managers import TaggableManager
import uuid 

# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")

        user = self.model(
            email=self.normalize_email(email),
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

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class District(models.Model):
    name =models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)

    def __str__(self):
        return str(self.name)

class Address(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    address1 = models.CharField(
        "Address line 1",
        max_length=1024, null=True,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024, null=True, blank=True
    )

    district =  models.ForeignKey(District, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return str(self.user)

class UserProfile(models.Model):
    GENDERS = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    STATUS = [
        ("pending", "Pending"),
        ("updated", "Updated"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, related_name="user_profiles")
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255 ,null=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=150, null=True, choices=GENDERS)
    update_status =  models.BooleanField(default=False)
    
    
    def __str__(self):
        return  str(self.first_name)
    
class Center (models.Model):

    name = models.CharField(max_length=150, null=True)
    center_abbreviation = models.CharField(max_length=20, null=True)
    district = models.ForeignKey(District, null=True, on_delete=models.DO_NOTHING)
    contact = models.CharField(max_length=150, null=True, blank=True)
    center_image = models.ImageField(upload_to='center_images',default="medical_center_default.jpg")
    address =  models.CharField(null=True, max_length=200)
    local_address =  models.CharField(null=True, max_length=200)
    center_description = models.TextField(max_length=10000, null=True, blank=True)
    
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.center_abbreviation


class ClinicEvent(models.Model):

    event_name = models.CharField(max_length=255, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=datetime.date.today, null=True)
    end_date = models.DateField(default=datetime.date.today, null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_expired = models.BooleanField(default=False, null=True)
    facility = models.ForeignKey(
        Center, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event_name) + " " + str(self.facility)
    
    def get_clinic_facility_long(self):
        return str(self.facility.name)
    
    def get_clinic_facility_short(self):
        return str(self.facility.center_abbreviation)
    
    def get_clinic_district(self):
         return str(self.facility.district.abbreviation)
    
    def get_clinic_district_long(self):
         return str(self.facility.district.name)
    
    
class NewsArticle(models.Model):
        title  = models.CharField(max_length=100, null=False)
        subtitle  = models.CharField(max_length=200, null=True,blank=True)
        date = models.DateTimeField(auto_now_add=True)
        body = models.TextField(max_length=10000, null=False)
        is_global = models.BooleanField(default=False, null=True)
        centers =  models.ManyToManyField(Center, blank=True)
        article_image = models.ImageField(upload_to='article_images', null=True, blank=True, default="annoucement.png")

        tags = TaggableManager(blank=True)

        def __str__(self):
            return str(self.title)

    
class OpeningTimes(models.Model):
    WEEKDAYS = [
    (0, ("Monday")),
    (1, ("Tuesday")),
    (2, ("Wednesday")),
    (3, ("Thursday")),
    (4, ("Friday")),
    (5, ("Saturday")),
    (6, ("Sunday")),
    (7, ("Holidays")),
    ]
    weekday = models.IntegerField(
        choices=WEEKDAYS
    )
    is_closed = models.BooleanField(default=False,null=True,blank=True,)
    from_hour = models.TimeField( null=True,blank=True,)
    to_hour = models.TimeField(null=True,blank=True,)
    center =  models.ManyToManyField(Center, blank=True)

    class Meta:
        verbose_name = 'Opening Time'
        verbose_name_plural = 'Opening Times'
        ordering = ["weekday"]

    def __str__(self):
            return str(str(self.get_weekday_display()) + " " + str(self.is_closed) + " " + str(self.from_hour) + " " + str(self.to_hour))
    