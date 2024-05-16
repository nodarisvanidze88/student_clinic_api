from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff status')
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('Superuser must have is_superuser status')
        return self.create_user(email,password,**extra_fields)
    

class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('doctor','Doctor'),
        ('patient','Patient'),
        ('manager', 'Manager')
    )
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','status']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    specialty = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Appoitment(models.Model):
    TREATMENT_DURATION_CHOICES = [
        (15, '15 minutes'),
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
    ]
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appoitments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appoitments')
    scheduled_time = models.DateTimeField()
    result = models.CharField(max_length=50)
    treatment_duration = models.IntegerField(choices=TREATMENT_DURATION_CHOICES)
    
    def get_end_time(self):
        return self.scheduled_time+timezone.timedelta(minutes=self.treatment_duration)
