from django.contrib import admin
from .models import Country, Cont_State, Financial_Year

# Register your models here.

admin.site.register(Country)
admin.site.register(Cont_State)
admin.site.register(Financial_Year)
