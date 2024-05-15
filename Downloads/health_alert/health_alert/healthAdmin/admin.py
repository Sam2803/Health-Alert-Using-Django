from django.contrib import admin
from .models import AdminUser,Clinic,Disease,Patient,Consultation

# Register your models here.
admin.site.register(AdminUser)
admin.site.register(Clinic)
admin.site.register(Disease)
admin.site.register(Patient)
admin.site.register(Consultation)
