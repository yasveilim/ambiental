from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.RestorePasswordRequest)
admin.site.register(models.AmbientalBook)
admin.site.register(models.AmbientalBookProps)
admin.site.register(models.UserSharepointDir)
admin.site.register(models.AmbientalBookSharepointPath)
