from django.db import models

# Create your models here.

class RestorePasswordRequest(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=50, null=True)
    reset_code = models.CharField(max_length=6, null=True)

class AmbientalBook(models.Model):
    material = models.CharField(max_length=50)
    document_name = models.CharField(max_length=50)
    is_critical = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    note = models.TextField()


class AmbientalBookProps(models.Model):
    book = models.ForeignKey(AmbientalBook, on_delete=models.CASCADE)
    ADVANCE_STATUS = [
        ("delivered", "DELIVERED"),
        ("pending", "PENDING"),
        ("na", "NA")
    ]
    archive = models.FileField(upload_to='uploads/')
    comment = models.TextField()
    advance = models.CharField(
        max_length=9, choices=ADVANCE_STATUS, default="pending")
    essential_in_cloud = models.BooleanField(default=True)
