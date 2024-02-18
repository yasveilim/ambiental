from django.db import models
import django.contrib.auth.models as User


class RestorePasswordRequest(models.Model):
    email = models.EmailField()
    # password = models.CharField(max_length=50, null=True)
    reset_code = models.CharField(max_length=6, null=True)


class AmbientalBookMaterial(models.Model):
    name = models.CharField(max_length=50)


class AmbientalBook(models.Model):
    material = models.ForeignKey(
        AmbientalBookMaterial, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=50)
    is_critical = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    note = models.TextField()


class AmbientalBookProps(models.Model):
    # NOTE: This can not be null
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(AmbientalBook, on_delete=models.CASCADE)
    ADVANCE_STATUS = [
        ("delivered", "DELIVERED"),
        ("pending", "PENDING"),
        ("na", "NA")
    ]
    archive = models.FileField(upload_to='uploads/')
    comment = models.TextField(default="")
    advance = models.CharField(
        max_length=9, choices=ADVANCE_STATUS, default="pending")
    essential_in_cloud = models.BooleanField(default=True)
