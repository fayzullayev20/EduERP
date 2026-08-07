from django.db import models
import uuid

class StudentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'        
    FROZEN = 'FROZEN', 'Frozen'        
    ARCHIVED = 'ARCHIVED', 'Archived'

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_regax = models.CharField(max_length=255)
    pasport_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    groups = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=StudentStatus.choices, default=StudentStatus.ACTIVE)
    balans = models.BigIntegerField(default=0)
    frozen_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    owner = models.UUIDField()

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"