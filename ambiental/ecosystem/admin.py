from django.contrib import admin
from .models import AmbientalBook, AmbientalBookProps

# Register your models here.
admin.site.register(AmbientalBook)
admin.site.register(AmbientalBookProps)