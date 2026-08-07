import uuid
from django.db import models


class StudentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    FROZEN = 'FROZEN', 'Frozen'
    ARCHIVED = 'ARCHIVED', 'Archived'


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    
    groups = models.ManyToManyField('groups.Group', related_name='enrolled_students', blank=True)
    status = models.CharField(
        max_length=50,
        choices=StudentStatus.choices,
        default=StudentStatus.ACTIVE
    )
    balance = models.BigIntegerField(default=0)
    
    frozen_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_students'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"