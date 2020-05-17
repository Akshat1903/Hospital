from django.contrib import admin
from .models import DoctorProfile,User,Patient
# Register your models here.

admin.site.register(DoctorProfile)
admin.site.register(Patient)
