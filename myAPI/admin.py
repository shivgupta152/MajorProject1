from django.contrib import admin
from .models import ContactForm, PatientInformation
# Register your models here.

admin.site.register(ContactForm)
admin.site.register(PatientInformation)
