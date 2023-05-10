from django.contrib import admin
from .models import Incident, CFSDistrict

# Register your models here.
admin.site.register(Incident)
admin.site.register(CFSDistrict)
