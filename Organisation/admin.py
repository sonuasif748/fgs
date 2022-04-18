from django.contrib import admin
from .models import Holidays, Organisation_Info, Department, Designation

# Register your models here.

admin.site.register(Organisation_Info)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Holidays)