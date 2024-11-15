from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message="Phone number must be entered in the format: '+9999999999'. Up to 10 digits allowed."
    )

    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    contact_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.username