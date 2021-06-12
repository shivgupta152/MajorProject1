from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ContactForm(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length = 300, blank=False)
    subject = models.CharField(max_length=300, blank=False)
    message = models.TextField(blank=False)


class PatientInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, default='Your Name')
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20,unique=True)
    email_id = models.EmailField(unique=False)
    address = models.TextField(blank=False)
    otp = models.CharField(max_length=8)
    aadhaar_card = models.CharField(max_length=14)
    date_time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50, default='NULL')
    x_ray = models.ImageField(upload_to='xray_images', default='C:/Users/HP/Documents/Chinnu/major_project_V1/majorProject_V1-main/media/COVID_19.png')

    def __str__(self):
        return self.name
