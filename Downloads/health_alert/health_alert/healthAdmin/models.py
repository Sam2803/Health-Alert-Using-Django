from django.db import models
import datetime

# Create your models here.
class AdminUser(models.Model):
    admin_id = models.AutoField
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    addDate = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return self.name

# Create your models here.
class Clinic(models.Model):
    clinic_id = models.AutoField
    name = models.CharField(max_length=100)
    doctorname = models.CharField(max_length=100)
    doctorqualification = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zipcode = models.IntegerField(default=0)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Disease(models.Model):
    disease_id = models.AutoField
    name = models.CharField(max_length=100)
    cure = models.TextField()
    precautions = models.TextField()
    symptoms = models.TextField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    patient_id = models.AutoField
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    pincode = models.IntegerField(default=0)
    address = models.CharField(max_length=30)
    addDate = models.DateField(default=datetime.date.today)
    clinicID = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Consultation(models.Model):
    consultation_id = models.AutoField
    patient = models.IntegerField(default=0)
    disease = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    clinicID = models.CharField(max_length=30)