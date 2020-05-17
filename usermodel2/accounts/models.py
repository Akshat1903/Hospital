from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.IntegerField(blank=True)
    speciality = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='accounts/profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact_no = models.IntegerField()
    address = models.CharField(max_length=200)
    dob = models.DateField()
    blood_group = models.CharField(max_length=3)
    case = models.TextField()
    report = models.ImageField(upload_to='accounts/patient_reports',blank=True)

    def __str__(self):
        return self.name
